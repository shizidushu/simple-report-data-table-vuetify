<template>
  <v-menu ref="menu" v-model="menu" v-bind="Object.assign({}, defaultAttrs.menu, $attrs.menu)">
    <template v-slot:activator="{ on }">
      <ValidationProvider :name="$attrs.label" :rules="rules" v-slot="{ errors, valid }">
        <v-text-field
          v-model="innerValue"
          v-bind="$attrs"
          v-on="{...$listeners, ...on}"
          :error-messages="errors"
          :success="valid"
        ></v-text-field>
      </ValidationProvider>
    </template>

    <v-time-picker
      v-model="innerValue"
      v-bind="Object.assign({}, defaultAttrs.timePicker, $attrs.timePicker)"
    >
      <v-spacer></v-spacer>
      <v-btn text color="primary" @click="menu = false">取消</v-btn>
      <v-btn text color="primary" @click="$refs.menu.save(innerValue)">确定</v-btn>
    </v-time-picker>
  </v-menu>
</template>

<script>
import { ValidationProvider } from "vee-validate";

export default {
  components: {
    ValidationProvider
  },
  props: {
    rules: {
      type: [Object, String],
      default: ""
    },
    value: {
      type: null
    }
  },
  data: () => ({
    innerValue: "",
    menu: false,
    defaultAttrs: {
      menu: {
        "close-on-content-click": false,
        "return-value.sync": "innerValue",
        transition: "scale-transition",
        "offset-y": true,
        "min-width": "290px"
      },
      timePicker: {
        "no-title": true,
        scrollable: true
      }
    }
  }),
  watch: {
    // Handles internal model changes.
    innerValue(newVal) {
      this.$emit("input", newVal);
    },
    // Handles external model changes.
    value(newVal) {
      this.innerValue = newVal;
    }
  },
  created() {
    if (this.value) {
      this.innerValue = this.value;
    }
  }
};
</script>
