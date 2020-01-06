import { required, email, max, max_value } from "vee-validate/dist/rules";
import { localize, extend } from "vee-validate";

extend("required", {
  ...required,
  message: "This field is required"
});

extend("max", {
  ...max,
  message: "This field must be {length} characters or less"
});

extend("email", {
  ...email,
  message: "This field must be a valid email"
});

extend("max_value", {
  ...max_value,
  message: "The max value of {_field_} is {max}"
})

import en from 'vee-validate/dist/locale/en.json';
import zh_CN from 'vee-validate/dist/locale/zh_CN.json';

// Install English and Arabic locales.
localize({
  zh_CN: {
    messages: zh_CN.messages,
    names: {
      email: "电子邮箱",
      password: "密码"
    },
    fields: {
      password: {
        required: "密码不可为空"
      }
    }
  },
  en
});

localize('zh_CN');
