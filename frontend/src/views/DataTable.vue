<template>
  <ValidationObserver
    ref="obs"
    v-slot="{ invalid, validated, passes, validate }"
  >
    <v-card>
      <v-card-title>{{ tableInfo.summary }}</v-card-title>
      <v-card-subtitle>
        <MarkdownDisplay :markdown="tableInfo.description" />
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-text>
        <v-form>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                md="6"
                v-for="(field, index) in formSchema"
                :key="index"
              >
                <component
                  :is="field.fieldType"
                  v-model="formData[field.name]"
                  v-bind="field"
                ></component>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="clear" :disabled="isEmptyformData">Clear</v-btn>
        <v-spacer></v-spacer>
        <v-btn @click="passes(submit)">Submit</v-btn>
      </v-card-actions>
      <v-divider></v-divider>
      <v-progress-linear :indeterminate="progressOn">
      </v-progress-linear>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="search"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-actions>
      <v-card-text>
        
        <v-data-table
          :headers="headers"
          :items="items"
          :search="search"
        ></v-data-table>
        
      </v-card-text>
    </v-card>
  </ValidationObserver>
</template>

<script>
import MarkdownDisplay from "@/components/MarkdownDisplay";
import { ValidationObserver, ValidationProvider } from "vee-validate";
import TTextField from "@/components/inputs/TTextField";
import TTextarea from "@/components/inputs/TTextarea";
import TSelect from "@/components/inputs/TSelect";
import TAutocomplete from "@/components/inputs/TAutocomplete";
import TCheckbox from "@/components/inputs/TCheckbox";
import TDatePicker from "@/components/inputs/TDatePicker";
import TTimePicker from "@/components/inputs/TTimePicker";
import request from "@/utils/request";

import { mapGetters } from "vuex";
export default {
  name: "DataTable",
  props: ["operationId"],
  components: {
    MarkdownDisplay,
    TTextField,
    TTextarea,
    TSelect,
    TAutocomplete,
    TCheckbox,
    TDatePicker,
    TTimePicker,
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      formData: {},
      search: "",
      headers: [],
      items: [],
      progressOn: null
    };
  },
  computed: {
    ...mapGetters(["data_table_path_info_of_current_user"]),
    tableInfo: function() {
      return this.data_table_path_info_of_current_user.find(i => {
        return i.operationId == this.operationId;
      });
    },
    formSchema: function() {
      return this.tableInfo.formSchema;
    },
    tableHeaders: function() {
      return [
        { text: "年", value: "年" },
        { text: "订单总金额USD", value: "订单总金额USD" },
        { text: "订单号", value: "订单号" }
      ]
    },
    isEmptyformData: function() {
      return (
        Object.entries(this.formData).length === 0 &&
        this.formData.constructor === Object
      );
    }
  },
  methods: {
    async clear() {
      this.formData = {};
      requestAnimationFrame(() => {
        this.$refs.obs.reset();
      });
    },
    async submit() {
      let res = await request({
        url: this.tableInfo.path.replace("/api/v1/", ""),
        method: this.tableInfo.method
      });
      this.items = res.data.items
      this.headers= res.data.headers
    }
  }
};
</script>
