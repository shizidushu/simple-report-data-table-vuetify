<template>
  <v-card>
    <v-card-title>
      Data Table List
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="tableHeaders"
      :items="tableItems"
      :search="search"
      class="tablelist"
    >
      <template v-slot:item.operationId="{ value }">
        <v-btn
          :to="{
            name: 'DataTable',
            params: { operationId: value }
          }"
          >View</v-btn
        >
      </template>

      <template v-slot:item.description="{ value }">
        <MarkdownDisplay :markdown="value" />
      </template>
    </v-data-table>
  </v-card>
</template>
<script>
import { mapGetters } from "vuex";
import MarkdownDisplay from "@/components/MarkdownDisplay";
export default {
  components: { MarkdownDisplay },
  data() {
    return {
      search: "",
      tableHeaders: [
        { text: "主题", value: "topic" },
        { text: "副主题", value: "subtopic" },
        { text: "名称", value: "summary" },
        { text: "描述", value: "description" },
        { text: "操作", value: "operationId" }
      ]
    };
  },
  computed: {
    ...mapGetters(["data_table_path_info_of_current_user"]),
    tableItems: function() {
      let items = this.data_table_path_info_of_current_user.map(function(item) {
        return item.infoItems;
      });
      return items;
    }
  }
};
</script>

<style>
.tablelist.theme--light .v-data-table-header tr {
  background-color: #80cbc4;
}
.tablelist.theme--dark .v-data-table-header tr {
  background-color: #616161;
}
</style>
