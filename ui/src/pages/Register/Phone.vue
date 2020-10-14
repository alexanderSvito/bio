<template>
  <Card class="card" :loading="isLoading">
    <div class="message">
        <h1>Verify your Phone</h1>
        In order to continue, please enter a code from SMS that we've just sent you.
        <PinCode @complete="codeReady" @incomplete="code = null" />
    </div>
    <v-btn
      block
      depressed
      color="primary"
      :disabled="!code"
      elevation="1"
      @click="isLoading = true"
      :loading="isLoading"
      large
    >Verify</v-btn>
  </Card>
</template>

<script>
import Card from "../../components/Card.vue"
import PinCode from "../../components/inputs/PinCode.vue"


export default {
  name: 'RegisterPhone',
  components: {
    Card,
    PinCode
  },
  data: () => {
    return {
      code: null,
      isLoading: false
    }
  },
  methods: {
    codeReady(code) {
      this.code = code;
    }
  }
}
</script>

<style scoped>
.card {
  width: 520px;
}

.message {
  padding: 25px;
}
</style>
