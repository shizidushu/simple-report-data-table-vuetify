import "material-design-icons-iconfont/dist/material-design-icons.css";
import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

// Translation provided by Vuetify (javascript)
import en from "vuetify/es5/locale/en";
import zhHans from "vuetify/es5/locale/zh-Hans";

export default new Vuetify({
  icons: {
    iconfont: "md"
  },
  lang: {
    locales: { zhHans, en },
    current: "zhHans"
  }
});
