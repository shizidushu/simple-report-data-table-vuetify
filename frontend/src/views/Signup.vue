<template>
  <v-container fill-height>
    <v-row align="center" justify="center">
      <v-col xs="12" sm="8" md="8" lg="6" xl="4">
        <v-card class="elevation-12">
          <v-toolbar color="blue">
            <v-toolbar-title>Signup form</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-alert :value="userExists" color="error" icon="warning"
                >This user already exists, try a different set of data.</v-alert
              >

              <v-text-field
                v-model="username"
                prepend-icon="person"
                name="login"
                label="Login"
                :rules="[rules.required]"
              ></v-text-field>

              <v-text-field
                v-model="email"
                prepend-icon="email"
                name="email"
                label="Email"
                :rules="[rules.required, rules.email]"
              ></v-text-field>

              <v-text-field
                v-model="password"
                prepend-icon="lock"
                name="password"
                label="Password"
                :rules="[rules.required]"
                type="password"
              ></v-text-field>

              <v-text-field
                v-model="confirm_password"
                prepend-icon="lock"
                name="password"
                label="Confirm Password"
                :rules="[rules.required]"
                type="password"
                :error="!valid()"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-divider light></v-divider>
          <v-card-actions>
            <v-btn to="/login" rounded color="black">Login</v-btn>
            <v-spacer></v-spacer>
            <v-btn rounded color="success" @click.prevent="register()">
              Register
              <v-icon>keyboard_arrow_right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Signup",
  data: () => ({
    userExists: false,
    username: "",
    email: "",
    password: "",
    confirm_password: "",
    rules: {
      required: value => !!value || "Required",
      email: value => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return pattern.test(value) || "Invalid e-mail.";
      }
    }
  }),
  methods: {
    valid() {
      return this.password === this.confirm_password;
    }
  }
};
</script>
