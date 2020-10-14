<template>
  <div class="main">
        <img class="back" src="../assets/back.svg">
        <div class="first-block">
            <h1>Ceteus</h1>
            <p>
                Ceteus is a free p2p-lending platform that helps you grow your funds.
            </p>
        </div>
        <div class="web">
            <img src="../assets/web.png">
        </div>
       <v-parallax src="../assets/logo.svg"></v-parallax>
       <v-card
           class="mx-auto"
           max-width="400"
           tile
         >
           <v-list-item>
             <v-list-item-content>
               <v-list-item-title>Single-line item</v-list-item-title>
             </v-list-item-content>
           </v-list-item>

           <v-list-item two-line>
             <v-list-item-content>
               <v-list-item-title>Two-line item</v-list-item-title>
               <v-list-item-subtitle>Secondary text</v-list-item-subtitle>
             </v-list-item-content>
           </v-list-item>

           <v-list-item three-line>
             <v-list-item-content>
               <v-list-item-title>Three-line item</v-list-item-title>
               <v-list-item-subtitle>
                 Secondary line text Lorem ipsum dolor sit amet,
               </v-list-item-subtitle>
               <v-list-item-subtitle>
                 consectetur adipiscing elit.
               </v-list-item-subtitle>
             </v-list-item-content>
           </v-list-item>
         </v-card>
  </div>
</template>

<script>
export default {
  name: 'Main',
  props: {
    msg: String
  },
  data: () => ({
    model: 0,
    colors: [
      'primary',
      'secondary',
      'yellow darken-2',
      'red',
      'orange',
    ],
  }),
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.main {
  width: 100%;
  position: relative;
}

.v-parallax {
  height: 1000px !important;

}

.first-block {
  position: absolute;
  top: 50px;
  left: 150px;
  color: white;

  font-family: 'Roboto';
  text-shadow: #090909 1px 1px 5px;

  & h1 {
    font-size: 100px;
  }

  & p {
    width: 600px;
    font-size: 48px;
  }
}


.web {
  position: absolute;
  top: 150px;
  right: 150px;
}

.back {
  object-fit: contain;
  width: 110%;
}
</style>
