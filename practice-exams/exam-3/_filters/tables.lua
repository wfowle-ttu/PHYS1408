--[[
Readable PDF tables for the exam-prep documents.

Pandoc's default LaTeX tables split the width evenly between columns and draw
no rules between body rows, so long wrapped cells run together. This filter
writes each table as a longtable instead:
  * column widths proportional to each column's longest cell (clamped),
  * a shaded, bold header row repeated on every page,
  * extra vertical padding and a light rule after every row.

Needs in the header: \usepackage{longtable,array,colortbl}
]]

local MIN_W, MAX_W = 4, 55 -- clamp on characters per column when sizing
local TEXT_PT = 505          -- 7in text block (letter paper, 0.75in margins)
local CHAR_PT = 5.6          -- rough width of one 11pt character
local CHAR_PT_BOLD = 6.6
local PAD_PT = 16            -- 2\tabcolsep plus a little slack

local ALIGN = {
  AlignLeft = "\\raggedright",
  AlignCenter = "\\centering",
  AlignRight = "\\raggedleft",
  AlignDefault = "\\raggedright",
}

local function cell_tex(cell)
  local tex = pandoc.write(pandoc.Pandoc(cell.contents), "latex")
  return (tex:gsub("%s+$", ""))
end

local function row_tex(row, bold)
  local parts = {}
  for _, cell in ipairs(row.cells) do
    local tex = cell_tex(cell)
    if bold and tex ~= "" then tex = "\\bfseries " .. tex end
    table.insert(parts, tex)
  end
  return table.concat(parts, " & ") .. " \\\\"
end

local function all_rows(tbl)
  local rows = {}
  for _, body in ipairs(tbl.bodies) do
    for _, r in ipairs(body.head) do table.insert(rows, r) end
    for _, r in ipairs(body.body) do table.insert(rows, r) end
  end
  return rows
end

function Table(tbl)
  if not FORMAT:match("latex") then return nil end

  local n = #tbl.colspecs
  local body = all_rows(tbl)
  local head = tbl.head.rows

  -- Size columns by their longest cell text, but never narrower than the
  -- longest single word (so short headers and words like "concept" are not
  -- clipped or hyphenated). Widths are worked out in points against a 7in
  -- text block and emitted as fractions of \linewidth.
  local len, word = {}, {}
  for j = 1, n do len[j], word[j] = MIN_W, 1 end
  local function measure(rows, bold)
    for _, r in ipairs(rows) do
      for j, cell in ipairs(r.cells) do
        local text = pandoc.utils.stringify(cell.contents)
        len[j] = math.max(len[j], math.min(utf8.len(text) or 0, MAX_W))
        for w in text:gmatch("%S+") do
          local pt = (utf8.len(w) or 0) * (bold and CHAR_PT_BOLD or CHAR_PT)
          word[j] = math.max(word[j], pt)
        end
      end
    end
  end
  measure(head, true)
  measure(body, false)

  local total = 0
  for j = 1, n do total = total + len[j] end
  local width, fixed, flex = {}, 0, 0
  for j = 1, n do
    local min_pt = word[j] + PAD_PT
    width[j] = len[j] / total * TEXT_PT
    if width[j] < min_pt then
      width[j] = min_pt
      fixed = fixed + min_pt
    else
      flex = flex + width[j]
    end
  end
  -- Shrink the wide columns to pay for any columns that were widened.
  local scale = flex > 0 and (TEXT_PT - fixed) / flex or 1
  for j = 1, n do
    if width[j] > word[j] + PAD_PT then width[j] = width[j] * scale end
  end

  local spec = {}
  for j, cs in ipairs(tbl.colspecs) do
    local frac = width[j] / TEXT_PT
    local align = ALIGN[tostring(cs[1])] or ALIGN[cs[1]] or "\\raggedright"
    table.insert(spec, string.format(
      ">{%s\\arraybackslash}p{\\dimexpr %.4f\\linewidth-2\\tabcolsep\\relax}", align, frac))
  end

  local out = {
    "\\begingroup",
    "\\renewcommand{\\arraystretch}{1.45}",
    "\\arrayrulecolor{black!25}",
    "\\begin{longtable}{" .. table.concat(spec) .. "}",
  }
  if #head > 0 then
    table.insert(out, "\\arrayrulecolor{black!60}\\hline\\arrayrulecolor{black!25}")
    for _, r in ipairs(head) do
      table.insert(out, "\\rowcolor{black!8}" .. row_tex(r, true))
    end
    table.insert(out, "\\arrayrulecolor{black!60}\\hline\\arrayrulecolor{black!25}")
    table.insert(out, "\\endhead")
  end
  for i, r in ipairs(body) do
    table.insert(out, row_tex(r, false))
    if i < #body then
      table.insert(out, "\\hline")
    else
      table.insert(out, "\\arrayrulecolor{black!60}\\hline")
    end
  end
  table.insert(out, "\\end{longtable}")
  table.insert(out, "\\endgroup")
  return pandoc.RawBlock("latex", table.concat(out, "\n"))
end
