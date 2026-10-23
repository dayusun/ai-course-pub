-- slide-dates.lua: stamp each slide with the date its source last changed.
--
-- The field moves fast, so every slide shows when its content was last edited.
-- The date comes from `git blame` on the .qmd: for each `##` slide, the newest
-- commit among the lines from its heading to the next heading. Lines not yet
-- committed count as today. Outside a git checkout no dates are added.
--
-- A shallow clone (CI's default) blames every line on one commit, so the dates
-- are only meaningful in a full-history checkout.

local function normalize(s)
  -- ASCII only: `%w` follows the C locale, which on Windows counts the bytes
  -- of curly quotes and non-breaking spaces as letters.
  return (s:lower():gsub("[^a-z0-9]", ""))
end

local function blame_dates(path)
  local dir = path:match("^(.*)[/\\]") or "."
  local file = path:match("([^/\\]+)$")
  -- Commits listed in .git-blame-ignore-revs (formatting or link-only passes)
  -- do not count as changes, so they don't reset every slide's date.
  local ignore = ""
  local top = io.popen(string.format('git -C "%s" rev-parse --show-toplevel', dir))
  if top then
    local root = top:read("*l")
    top:close()
    local revs = root and (root .. "/.git-blame-ignore-revs")
    local fh = revs and io.open(revs, "r")
    if fh then
      fh:close()
      ignore = string.format(' --ignore-revs-file "%s"', revs)
    end
  end
  local cmd = string.format('git -C "%s" blame --line-porcelain%s -- "%s"', dir, ignore, file)
  local pipe = io.popen(cmd)
  if not pipe then return nil end

  local dates, line_no, time = {}, nil, nil
  for row in pipe:lines() do
    local final = row:match("^%x+ %d+ (%d+)")
    if final and #row:match("^(%x+)") == 40 then
      line_no = tonumber(final)
    elseif row:match("^committer%-time ") then
      time = tonumber(row:match("(%d+)$"))
    elseif row:sub(1, 1) == "\t" and line_no and time then
      dates[line_no] = time
    end
  end
  pipe:close()
  if next(dates) == nil then return nil end
  return dates
end

-- Map each slide heading (normalized text) to the newest time in its range.
local function heading_times(path, dates)
  local lines, in_fence = {}, false
  for line in io.lines(path) do lines[#lines + 1] = line end

  local starts = {}
  for i, line in ipairs(lines) do
    if line:match("^```") or line:match("^~~~") then in_fence = not in_fence end
    if not in_fence and line:match("^##? ") then starts[#starts + 1] = i end
  end

  local result = {}
  for k, first in ipairs(starts) do
    local last = (starts[k + 1] or (#lines + 1)) - 1
    local newest = 0
    for i = first, last do
      if dates[i] and dates[i] > newest then newest = dates[i] end
    end
    local text = lines[first]:gsub("^##? ", ""):gsub("%s*{[^}]*}%s*$", "")
    local key = normalize(text)
    if newest > 0 and (result[key] == nil or newest > result[key]) then
      result[key] = newest
    end
  end
  return result
end

function Pandoc(doc)
  local path = quarto and quarto.doc and quarto.doc.input_file
  if not path then return doc end
  local dates = blame_dates(path)
  if not dates then return doc end
  local times = heading_times(path, dates)

  local blocks = pandoc.List()
  for _, block in ipairs(doc.blocks) do
    blocks:insert(block)
    if block.t == "Header" and block.level == 2 then
      local t = times[normalize(pandoc.utils.stringify(block.content))]
      if t then
        blocks:insert(pandoc.RawBlock("html",
          '<div class="slide-date">Updated ' .. os.date("%Y-%m-%d", t) .. "</div>"))
      end
    end
  end
  doc.blocks = blocks
  return doc
end
