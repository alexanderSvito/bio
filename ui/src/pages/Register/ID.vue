<template>
  <Card class="message">
    <h1>Almost there!</h1>
    In order ro continue, we need your identity proof. Please, provide photos of yourself and your documents.
    <web-cam ref="camera" :autoplay="true" />
    <v-btn
      block
      depressed
      color="primary"
      elevation="1"
      @click="start"
      large
    >Start</v-btn>
  </Card>
</template>

<script>
import Card from "../../components/Card.vue"
import { WebCam } from "vue-web-cam"


export default {
  name: 'RegisterID',
  components: {
    Card,
    WebCam
  },
  methods: {
    start () {
       console.log(this.$refs['camera']);
       this.$refs['camera'].start();
    }
  }
}
</script>

<style scoped>
.message {
  width: 520px;
  padding: 20px;
}
</style>
