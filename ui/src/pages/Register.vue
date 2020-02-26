<template>
  <div>
      <Card class="form">
        <div class="formfield">
          <v-row>
            <v-col cols="12" sm="12" md="6">
              <v-text-field
                label="Имя"
                color="#00b09b"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="12" md="6">
              <v-text-field
                label="Фамилия"
                color="#00b09b"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12" md="12">
              <v-text-field
                label="Email"
                type="email"
                color="#00b09b"
                prepend-icon="mdi-email"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="d-flex" cols="12" sm="6">
              <v-select
                :items="classes"
                label="Класс"
                color="#00b09b"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12" md="12">
              <v-text-field
                label="Пароль"
                type="password"
                color="#00b09b"
              ></v-text-field>
            </v-col>
          </v-row>
        </div>


      </Card>
  </div>
</template>

<script>
import Card from '../components/Card.vue'

export default {
  name: 'Main',
  components: {
    Card
  },
  data: () => {
    return {
      classes: [
        'А', 'Б', 'В', 'Г', 'Д'
      ]
    }
  }
}
</script>

<style scoped>
.form {
  width: 540px;
}
.formfield {
  padding: 20px;
}
</style>
