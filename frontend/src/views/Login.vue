/* eslint-disable */
<template>
  <v-container fill-height>
    <v-row align="center" justify="center">
      <v-col xs="12" sm="8" md="8" lg="6" xl="4">
        <v-form>
          <v-card class="elevation-12">
            <v-toolbar color="blue">
              <v-toolbar-title>Login form</v-toolbar-title>
            </v-toolbar>
            <v-alert
              color="error"
              :value="error"
              icon="close"
            >The username or the password are incorrect.</v-alert>
            <v-card-text>
              <v-text-field
                v-model="username"
                prepend-icon="person"
                name="login"
                label="Login"
                :rules="[rules.required]"
              ></v-text-field>

              <v-text-field
                v-model="password"
                prepend-icon="lock"
                name="password"
                label="Password"
                :rules="[rules.required]"
                type="password"
              ></v-text-field>
            </v-card-text>
            <v-divider light></v-divider>

            <v-card-actions>
              <v-btn to="/signup" rounded color="indigo">Sign up</v-btn>
              <v-spacer></v-spacer>
              <v-btn rounded color="primary" @click.prevent="login()">
                Login
                <v-icon>keyboard_arrow_right</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Login",
  data: () => ({
    username: "",
    password: "",
    error: false,
    rules: {
      required: value => !!value || "Required"
    }
  }),
  methods: {
    login() {
      this.$store
        .dispatch("user/login", {playload: {
          username: this.username,
          password: this.password
        }, routes: this.$router.options.routes} )
        // eslint-disable-next-line
        .then(success => {
          this.$router.push("/");
        })
        // eslint-disable-next-line
        .catch(error => {
          this.error = true;
        });
    }
  }
};
</script>
