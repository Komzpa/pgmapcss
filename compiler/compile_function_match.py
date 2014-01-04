def compile_function_match(id, stat):
    replacement = {
      'style_id': id
    }

    ret = '''\
create or replace function {style_id}_match(
  render_context\tpgmapcss_render_context,
  "all-style-elements"\ttext[] default Array['default']
) returns setof pgmapcss_result as $body$
declare
  ret pgmapcss_result;
  "max-style-element" int;
  t timestamp with time zone; -- profiling
begin
  t := clock_timestamp(); -- profiling
  "max-style-element" := array_upper("all-style-elements", 1);
  return query
    select * from (
    select
      id, tags, geo, types, pseudo_element, properties,
      unnest("all-style-elements") as "style-element"
    from
      (select (result).* from
        (select
          (CASE WHEN (result).combine_type is null THEN (array_agg(result))[1]
          ELSE {style_id}_check(
            pgmapcss_object(string_agg((result).id, ';'), hstore_merge(array_agg((result).tags)), ST_Collect((result).geo), Array[(result).combine_type]), render_context)
          END) result from
        (select
          {style_id}_check(
            object, render_context
          ) result
        from
          objects(render_context, {style_id}_get_where(render_context)) object
        offset 0) t
        group by (result).combine_type, coalesce((result).combine_id, (result).id || (result).pseudo_element) offset 0) t) t
        order by
          pgmapcss_to_float(properties->'layer') asc,
          generate_series(1, "max-style-element") asc,
          coalesce(cast(properties->'z-index' as float), 0) asc
        ) t where
          (select true = any(array_agg(x is not null)) from (select unnest(properties->(cast(' || quote_nullable(stat.prop_style_element) || E'->("style-element") as text[]))) x) t1) or not ' || quote_nullable(stat.prop_style_element) || E'? ("style-element");
    raise notice 'total run of match() (incl. querying db objects) took %', clock_timestamp() - t; -- profiling
    return;
end;
$body$ language 'plpgsql' immutable;
'''.format(**replacement);

    return ret
