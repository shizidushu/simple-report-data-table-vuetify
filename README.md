# simple-report-data-table-vuetify

A simple web to serve data table. It is built with Vuetify, Vue, FastApi.


The main features:

- RBAC with casbin
- simple data table with vuetify's component
- dynamically forms based on data from api
- Automatic generated permission name based on API route tags
- Use Mongodb as database
- Use FastApi

How to run:
- cd frontend; npm run serve
- cd backend; uvicorn app.main:app --reload



When build this project, I borrow a lot of ideas or codes from blog posts and repository. Thanks. Here is a list (not full):

- https://rangle.io/blog/how-to-create-data-driven-user-interfaces-in-vue/
- https://github.com/PanJiaChen/vue-element-admin
- https://github.com/MuhaddiMu/VuetiForm
- https://github.com/markqiu/fastapi-mongodb-realworld-example-app
- https://github.com/tiangolo/full-stack-fastapi-postgresql
- https://github.com/jeffreybiles/vue-screencasts
- https://github.com/you-dont-need/You-Dont-Need-Lodash-Underscore