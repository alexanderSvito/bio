<template>
    <div class="container">
        <h1 v-if="user.first_name">Welcome, {{ user.first_name }}!</h1>
        <h1 v-else>Registration Form</h1>
        <div class="form">
        <div class="formfield">
            <v-form
                ref="form"
                v-model="valid"
                lazy-validation
             >
          <v-row align="center" class="general">
            <v-col cols="12" sm="12" md="6">
              <v-text-field
                label="First Name"
                placeholder="John"
                v-model="user.first_name"
                :rules="[() => !!user.first_name || 'This field is required']"
                color="secondary"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="12" md="6">
              <v-text-field
                label="Last Name"
                placeholder="Doe"
                v-model="user.last_name"
                :rules="[() => !!user.last_name || 'This field is required']"
                color="secondary"
                required
              ></v-text-field>
            </v-col>

            <v-row cols="12" sm="12" md="12" align="center" class="align">
                <v-checkbox
                    v-model="user.has_other_names"
                    style="margin-left: 8px;"
                    hide-details
                    color="secondary"
                    class="shrink mr-2 mt-0"
                  ></v-checkbox>
                  <v-text-field
                    :disabled="!user.has_other_names"
                    label="Other names"
                    v-model="user.other_name"
                    placeholder="Middle name"
                    color="secondary"
                  ></v-text-field>

             </v-row>

                <v-col cols="12" sm="12" md="12">
              <v-text-field
                          label="Email"
                          type="email"
                          v-model="user.email"
                          color="secondary"
                          :rules="[() => !!user.email || 'This field is required']"
                          placeholder="sample@mail.com"
                          prepend-inner-icon="mdi-email"
                          required
                        ></v-text-field>
                </v-col>
                <v-col>
                <Phone v-model="user.phone" :errors="errors['phone']" />
                </v-col>
            </v-row>


            <v-row class="general">
                <v-col cols="12" sm="12" md="12">
                    <label class="v-label" for="gdnr">
                      Your Gender
                    </label>
                </v-col>

                <v-col class="tight" cols="12" sm="12" md="12">
                    <v-radio-group
                      v-model="user.gender"
                      :rules="[() => !!user.gender || 'Please, choose one']"
                      id="gdnr"
                      row
                      required
                    >

                      <v-radio
                        label="Male"
                        value="male"
                        color="secondary"
                      >
                        <template v-slot:label>
                          <div>It's <span class="secondary--text">Male</span></div>
                        </template>
                      </v-radio>
                      <v-radio
                        label="Female"
                        value="female"
                        color="accent"
                      >
                        <template v-slot:label>
                          <div>It's <span class="accent--text">Female</span></div>
                        </template>
                      </v-radio>

                    </v-radio-group>
                </v-col>
            </v-row>



            <v-row>
                <v-col>
                    <v-text-field
                        ref="address"
                        v-model="user.addresses.address_1"
                        :rules="[
                        () => !!user.addresses.address_1 || 'This field is required',
                        () => !!user.addresses.address_1 && user.addresses.address_1.length <= 25 || 'Address must be less than 25 characters'
                        ]"
                        label="Address Line"
                        autocomplete="disabled"
                        color="secondary"
                        placeholder="Snowy Rock Pl"
                        counter="25"
                        required
                    ></v-text-field>
                    <v-text-field
                        ref="address_2"
                        v-model="user.addresses.address_2"
                        label="Address Line #2"
                        autocomplete="disabled"
                        color="secondary"
                        hint="Optional"
                        placeholder="55-17"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-text-field
              ref="city"
              v-model="user.addresses.city"
              color="secondary"
              :rules="[() => !!user.addresses.city || 'This field is required']"
              label="City"
              autocomplete="disabled"
              placeholder="El Paso"
              required
            ></v-text-field>
            <v-text-field
              ref="state"
              v-model="user.addresses.state"
              color="secondary"
              autocomplete="disabled"
              :rules="[() => !!user.addresses.state || 'This field is required']"
              label="State/Province/Region"
              required
              placeholder="TX"
            ></v-text-field>
            <v-text-field
              ref="zip"
              v-model="user.addresses.zip"
              color="secondary"
              autocomplete="disabled"
              :rules="[() => !!user.addresses.zip || 'This field is required']"
              label="ZIP / Postal Code"
              required
              placeholder="79938"
            ></v-text-field>
            <v-row>
            <v-col>
            <v-autocomplete
              ref="country"
              v-model="user.addresses.country"
              color="secondary"
              autocomplete="disabled"
              :rules="[() => !!user.addresses.country || 'This field is required']"
              :items="countries"
              label="Country"
              placeholder="Select..."
              required
            ></v-autocomplete>
            </v-col>
            </v-row>
            </v-form>
        </div>

        <v-btn
          block
          depressed
          color="primary"
          elevation="1"
          @click="sendData"
          :loading="isLoading"
          large
        >Complete</v-btn>
    </div>
  </div>
</template>

<script>
import config from "../../config"
import Phone from "../../components/inputs/Phone.vue"

export default {
  name: 'Main',
  components: {
    Phone
  },
  data: () => {
    return {
      valid: true,
      errors: {},
      user: {
          has_other_names: false,
          first_name: '',
          last_name: '',
          other_name: '',
          gender: null,
          phone: '',
          email: '',
          addresses: {
              address_1: '',
              address_2: '',
              city: '',

              state: '',
              zip: '',
              country: '',
          }
      },
      isLoading: false,
      isError: false,
      countries: ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua & Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia & Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Cape Verde', 'Cayman Islands', 'Chad', 'Chile', 'China', 'Colombia', 'Congo', 'Cook Islands', 'Costa Rica', 'Cote D Ivoire', 'Croatia', 'Cruise Ship', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia', 'French West Indies', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyz Republic', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint Pierre &amp; Miquelon', 'Samoa', 'San Marino', 'Satellite', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'St Kitts &amp; Nevis', 'St Lucia', 'St Vincent', 'St. Lucia', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', "Timor L'Este", 'Togo', 'Tonga', 'Trinidad &amp; Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks &amp; Caicos', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Virgin Islands (US)', 'Yemen', 'Zambia', 'Zimbabwe'],

    }
  },
  methods: {
    sendData () {
      this.isLoading = true;
      if (this.$refs.form.validate()) {
        this.valid = true;
        let that = this;
        this.$http.post(config.HOST + '/verify/email', this.user).then(
          (response) => {
            this.$store.commit('setUser', { user: response.data });
            that.$router.push('/register/email');
          }
        ).catch(
          (e) => {
            this.errors = e.response.data;
            this.valid = false;
            this.isLoading = false;
          }
        );
      } else {
        this.isError = true;
        this.isLoading = false;
      }

   }
  }
}
</script>

<style scoped>
.form {
  width: 540px;
  font-family: 'Lato';
  background: white;
  margin: 30px;

  line-height: 1.5em;

  border-top: black 2px solid;
}
.formfield {
  padding: 20px;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 1;
}

h1 {
  margin-top: 20px;
}

.general {
  margin-top: 12px;
}

.general * {
  padding-bottom: 0;
}

.tight {
  padding-top: 0;
}

.general .v-input--radio-group, .v-input__slot {
  margin-top: 0;
  margin-bottom: 0;
}

.align {
  padding-left: 14px;
  padding-right: 22px;
}
</style>

<style>

</style>
