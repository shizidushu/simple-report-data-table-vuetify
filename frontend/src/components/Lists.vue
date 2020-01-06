<template>
  <v-navigation-drawer permanent app style="overflow: hidden">
    <v-app-bar color="blue" app clipped-left>
      <v-toolbar-title>Your lists</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>search</v-icon>
      </v-btn>
    </v-app-bar>

    <v-banner color="blue" sticky tile elevation="10">
      Create a new list
      <template v-slot:actions>
        <v-btn icon>
          <v-icon>add</v-icon>
        </v-btn>
      </template>
    </v-banner>

    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Create a new list</v-list-item-title>
        </v-list-item-content>

        <v-list-item-action>
          <v-btn icon>
            <v-icon>add</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>

    <v-list>
      <v-list-item v-for="(list, key) in lists" :key="key">
        <v-list-item-content>
          <v-list-item-title>{{ list.title }}</v-list-item-title>
        </v-list-item-content>

        <v-list-item-action>
          <v-list-item-title>{{ list.tasks }}</v-list-item-title>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "Lists",
  data: () => ({
    lists: [
      {
        id: 1,
        title: "List",
        tasks: 12
      },
      {
        id: 1,
        title: "List",
        tasks: 45
      },
      {
        id: 1,
        title: "List",
        tasks: 66
      },
      {
        id: 1,
        title: "List",
        tasks: 3
      },
      {
        id: 1,
        title: "List",
        tasks: 12
      },
      {
        id: 1,
        title: "List",
        tasks: 45
      },
      {
        id: 1,
        title: "List",
        tasks: 66
      },
      {
        id: 1,
        title: "List",
        tasks: 3
      },
      {
        id: 1,
        title: "List",
        tasks: 12
      },
      {
        id: 1,
        title: "List",
        tasks: 45
      },
      {
        id: 1,
        title: "List",
        tasks: 66
      },
      {
        id: 1,
        title: "List",
        tasks: 3
      },
      {
        id: 1,
        title: "List",
        tasks: 12
      },
      {
        id: 1,
        title: "List",
        tasks: 45
      },
      {
        id: 1,
        title: "List",
        tasks: 66
      },
      {
        id: 1,
        title: "List",
        tasks: 3
      },
      {
        id: 1,
        title: "List",
        tasks: 12
      },
      {
        id: 1,
        title: "List",
        tasks: 45
      },
      {
        id: 1,
        title: "List",
        tasks: 66
      },
      {
        id: 1,
        title: "List",
        tasks: 3
      }
    ]
  })
};
</script>
