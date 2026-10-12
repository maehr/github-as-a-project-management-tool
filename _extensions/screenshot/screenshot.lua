-- Shortcode {{< screenshot NAME >}} or {{< screenshot NAME nocaption >}}
-- Builds a figure from assets/screenshots/annotations.yml: the image, its alt
-- text, and a caption that lists the numbered callouts and the capture date.
-- With "nocaption", the figure has no caption. The slides use it, because the
-- callout list does not fit on a slide. The image itself still states the
-- capture date in its caption bar.

local spec = nil

local function load_spec()
  if spec then
    return spec
  end
  local path = quarto.project.directory .. "/assets/screenshots/annotations.yml"
  local handle = io.open(path, "r")
  if handle == nil then
    error("screenshot: cannot read " .. path)
  end
  local text = handle:read("a")
  handle:close()
  local meta = pandoc.read("---\n" .. text .. "\n---\n", "markdown").meta
  spec = { captured = pandoc.utils.stringify(meta.captured), shots = {} }
  for _, shot in ipairs(meta.screenshots) do
    local name = pandoc.utils.stringify(shot.file):gsub("%.webp$", "")
    spec.shots[name] = shot
  end
  return spec
end

return {
  ["screenshot"] = function(args)
    local name = pandoc.utils.stringify(args[1])
    local data = load_spec()
    local shot = data.shots[name]
    if shot == nil then
      error("screenshot: no entry '" .. name .. "' in annotations.yml")
    end
    local alt = pandoc.utils.stringify(shot.alt)
    local parts = {}
    for index, callout in ipairs(shot.callouts or {}) do
      table.insert(parts, "(" .. index .. ") " .. pandoc.utils.stringify(callout.label))
    end
    local captured = shot.captured and pandoc.utils.stringify(shot.captured) or data.captured
    local caption = table.concat(parts, "; ") .. ". Captured " .. captured .. "."
    local offset = quarto.project.offset or "."
    local src = offset .. "/assets/screenshots/" .. pandoc.utils.stringify(shot.file)
    local image = pandoc.Image(pandoc.Inlines(alt), src, "")
    local long = { pandoc.Plain(pandoc.Inlines(caption)) }
    if args[2] and pandoc.utils.stringify(args[2]) == "nocaption" then
      long = {}
    end
    local figure = pandoc.Figure(pandoc.Plain({ image }), { long = long }, { id = "fig-" .. name })
    return pandoc.Blocks({ figure })
  end,
}
