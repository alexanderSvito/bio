<template>
  <Card class="message">
    <h1>Thank you for registration!</h1>
    In order ro continue, please visit a link we've just sent to your email.
  </Card>
</template>

<script>
import Card from "../../components/Card.vue"

export default {
  name: 'RegisterEmail',
  components: {
    Card
  }
}
</script>

<style scoped>
.message {
  width: 520px;
  padding: 20px;
}
</style>
