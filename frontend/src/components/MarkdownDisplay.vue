<template>
  <div v-html="processedMarkdown"></div>
</template>

<script>
import { convert_text } from "@/api/tool";
export default {
  props: {
    markdown: String
  },
  data() {
    return {
      processedMarkdown: ""
    };
  },
  watch: {
    markdown: {
      async handler(val) {
        if (val) {
          let response = await convert_text({
            source: val,
            to: "html",
            format: "md"
          });
          this.processedMarkdown = response.data;
        } else {
          this.processedMarkdown = "";
        }
      },
      immediate: true,
      deep: true
    }
  }
};
</script>
