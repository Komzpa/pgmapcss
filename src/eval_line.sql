create or replace function eval_line(param text[],
  object pgmapcss_object, current pgmapcss_current, render_context pgmapcss_render_context)
returns text
as $$
#variable_conflict use_variable
declare
  list text[];
begin
  if array_upper(param, 1) > 1 then
    list := param;
  else
    list := string_to_array(param[1], ';');
  end if;

  if array_upper(param, 1) < 2 then
    return '';
  end if;

  return ST_MakeLine(list);
end;
$$ language 'plpgsql' immutable;


