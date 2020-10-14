<template>
  <v-row align="center" class="pincode">
      <v-col v-for="n in 6" :key="n" cols="12" sm="12" md="2">
        <v-text-field
          :ref="'num-' + n"
          placeholder="0"
          type="number"
          class="pin"
          min="0"
          maxlength="1"
          color="secondary"
          max="9"
          @keydown="beforeInput"
          @keyup="inputNext"
          required
        ></v-text-field>
      </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'Phone',
  props: ['errors'],
  computed: {
      code() {
        let res = '';
        for (let i = 1; i < 7; i++) {
            let el = this.$refs['num-' + i][0].$refs['input'];
            res += el.value;
        }
        return res;
      }
  },
  methods: {
    beforeInput(event) {
      if (event.target.value.length != 0 && event.keyCode != 8) {
        event.preventDefault()
      }
    },
    firstEmpty() {
      for (let i = 1; i < 7; i++) {
        let el = this.$refs['num-' + i][0].$refs['input'];
        console.log(el.value);
        if (el.value.length == 0) {
          return el;
        }
      }
      return null;
    },
    inputNext() {
      const el = this.firstEmpty();
      if (el !== null) {
        this.$emit('incomplete');
        el.focus();
      } else {
        this.$emit('complete', this.code);
      }
    }
  }
}
</script>

<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type="number"] {
  -moz-appearance: textfield;
}

.v-text-field.pin input {
  font-size: 32px;
  text-align: center;
}
</style>

<style scoped>

.pincode {
   margin-left: auto;
   margin-right: auto;
   width: 80%;
}
</style>
