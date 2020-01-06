const axios = require("axios");

axios.get(`http://127.0.0.1:8000/openapi.json`).then(response => {
  const { data } = response;
  //   console.log(data);
  const { paths, tags } = data;

  let report_paths = [];
  for (p in paths) {
    single_path = paths[p];

    for (m in single_path) {
      single_method = single_path[m];

      if (!single_method.tags.includes("report")) delete single_path[m];
    }

    if (Object.keys(single_path).length == 0) {
      delete paths[p];
    }

    for (m in single_path) {
      single_path[m]["tags"].splice(
        single_path[m]["tags"].indexOf("report"),
        1
      );

      report_paths.push({
        ...single_path[m],
        path: p.replace("/api/v1/", ""),
        method: m
      });
    }
  }

  report_paths.map(function(item) {
    item.topic = item.tags.pop();

    let has_topic_doc = tags.find(t => t.name == item.topic);
    if (has_topic_doc) {
      item.topic = has_topic_doc.description;
    }

    item.subtopic = item.tags.pop();

    let has_subtopic_doc = tags.find(t => t.name == item.subtopic);
    if (has_subtopic_doc) {
      item.subtopic = has_subtopic_doc.description;
    }

    delete item.tags;
    // console.log(item.topic)
  });

  report_paths.map(function(item) {
    if (item.parameters) {
      // console.log(true);
      item.formatInputSchema = [];
      item.parameters.map(function(param) {
        if (param.schema.additionalProperties) {
          let paramSchema = Object.assign(
            {},
            { name: param.name },
            param.schema.additionalProperties
          );
          item.formatInputSchema.push(paramSchema);
        }
      });
      // console.log(item.formatInputSchema);
    }
  });

  // console.log(report_paths);

  return report_paths;
});
