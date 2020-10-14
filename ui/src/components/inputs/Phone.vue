<template>
  <v-row align="center" class="general">
      <v-col cols="12" sm="12" md="3">
        <v-autocomplete
          :label="getLabel"
          placeholder="1"
          type="number"
          autocomplete="disabled"
          :items="digits"
          v-model="code"
          :value="getCode"
          :rules="[() => !!code || 'Select code']"
          color="secondary"
          @input="emitValue"
          required
        >
            <v-icon slot="prepend-inner" style="margin-top: 3.5px;" small dense>
              mdi-plus
            </v-icon>
        </v-autocomplete>
      </v-col>

      <v-col cols="12" sm="12" md="9">
        <v-text-field
          label="Phone"
          placeholder="555-123-456"
          v-mask="'###-###-#####'"
          v-model="phone"
          type="tel"
          :value="getPhone"
          :rules="[() => !!phone || 'This field is required', () => !errors || errors[0]]"
          color="secondary"
          @input="emitValue"
          required
        ></v-text-field>
      </v-col>


  </v-row>
</template>

<script>
export default {
  name: 'Phone',
  props: ['value', 'errors'],
  computed: {
    digits() {
      return Object.keys(this.codes)
    },
    getLabel() {
      if (this.code === null) {
        return 'Code'
      } else {
        return this.codes[this.code]['name']
      }
    },
    getCode() {
      return this.value.split(" ")[0]
    },
    getPhone() {
      return this.value.split(" ")[1]
    }
  },
  data: () => {
      return {
        code: null,
        phone: '',
        codes: {'972': {'code': 'IL', 'name': 'Israel'}, '93': {'code': 'AF', 'name': 'Afghanistan'}, '355': {'code': 'AL', 'name': 'Albania'}, '213': {'code': 'DZ', 'name': 'Algeria'}, '1 684': {'code': 'AS', 'name': 'AmericanSamoa'}, '376': {'code': 'AD', 'name': 'Andorra'}, '244': {'code': 'AO', 'name': 'Angola'}, '1 264': {'code': 'AI', 'name': 'Anguilla'}, '1268': {'code': 'AG', 'name': 'Antigua and Barbuda'}, '54': {'code': 'AR', 'name': 'Argentina'}, '374': {'code': 'AM', 'name': 'Armenia'}, '297': {'code': 'AW', 'name': 'Aruba'}, '61': {'code': 'CC', 'name': 'Cocos (Keeling) Islands'}, '43': {'code': 'AT', 'name': 'Austria'}, '994': {'code': 'AZ', 'name': 'Azerbaijan'}, '1 242': {'code': 'BS', 'name': 'Bahamas'}, '973': {'code': 'BH', 'name': 'Bahrain'}, '880': {'code': 'BD', 'name': 'Bangladesh'}, '1 246': {'code': 'BB', 'name': 'Barbados'}, '375': {'code': 'BY', 'name': 'Belarus'}, '32': {'code': 'BE', 'name': 'Belgium'}, '501': {'code': 'BZ', 'name': 'Belize'}, '229': {'code': 'BJ', 'name': 'Benin'}, '1 441': {'code': 'BM', 'name': 'Bermuda'}, '975': {'code': 'BT', 'name': 'Bhutan'}, '387': {'code': 'BA', 'name': 'Bosnia and Herzegovina'}, '267': {'code': 'BW', 'name': 'Botswana'}, '55': {'code': 'BR', 'name': 'Brazil'}, '246': {'code': 'IO', 'name': 'British Indian Ocean Territory'}, '359': {'code': 'BG', 'name': 'Bulgaria'}, '226': {'code': 'BF', 'name': 'Burkina Faso'}, '257': {'code': 'BI', 'name': 'Burundi'}, '855': {'code': 'KH', 'name': 'Cambodia'}, '237': {'code': 'CM', 'name': 'Cameroon'}, '1': {'code': 'US', 'name': 'United States'}, '238': {'code': 'CV', 'name': 'Cape Verde'}, ' 345': {'code': 'KY', 'name': 'Cayman Islands'}, '236': {'code': 'CF', 'name': 'Central African Republic'}, '235': {'code': 'TD', 'name': 'Chad'}, '56': {'code': 'CL', 'name': 'Chile'}, '86': {'code': 'CN', 'name': 'China'}, '57': {'code': 'CO', 'name': 'Colombia'}, '269': {'code': 'KM', 'name': 'Comoros'}, '242': {'code': 'CG', 'name': 'Congo'}, '682': {'code': 'CK', 'name': 'Cook Islands'}, '506': {'code': 'CR', 'name': 'Costa Rica'}, '385': {'code': 'HR', 'name': 'Croatia'}, '53': {'code': 'CU', 'name': 'Cuba'}, '537': {'code': 'CY', 'name': 'Cyprus'}, '420': {'code': 'CZ', 'name': 'Czech Republic'}, '45': {'code': 'DK', 'name': 'Denmark'}, '253': {'code': 'DJ', 'name': 'Djibouti'}, '1 767': {'code': 'DM', 'name': 'Dominica'}, '1 849': {'code': 'DO', 'name': 'Dominican Republic'}, '593': {'code': 'EC', 'name': 'Ecuador'}, '20': {'code': 'EG', 'name': 'Egypt'}, '503': {'code': 'SV', 'name': 'El Salvador'}, '240': {'code': 'GQ', 'name': 'Equatorial Guinea'}, '291': {'code': 'ER', 'name': 'Eritrea'}, '372': {'code': 'EE', 'name': 'Estonia'}, '251': {'code': 'ET', 'name': 'Ethiopia'}, '298': {'code': 'FO', 'name': 'Faroe Islands'}, '679': {'code': 'FJ', 'name': 'Fiji'}, '358': {'code': 'FI', 'name': 'Finland'}, '33': {'code': 'FR', 'name': 'France'}, '594': {'code': 'GF', 'name': 'French Guiana'}, '689': {'code': 'PF', 'name': 'French Polynesia'}, '241': {'code': 'GA', 'name': 'Gabon'}, '220': {'code': 'GM', 'name': 'Gambia'}, '995': {'code': 'GE', 'name': 'Georgia'}, '49': {'code': 'DE', 'name': 'Germany'}, '233': {'code': 'GH', 'name': 'Ghana'}, '350': {'code': 'GI', 'name': 'Gibraltar'}, '30': {'code': 'GR', 'name': 'Greece'}, '299': {'code': 'GL', 'name': 'Greenland'}, '1 473': {'code': 'GD', 'name': 'Grenada'}, '590': {'code': 'MF', 'name': 'Saint Martin'}, '1 671': {'code': 'GU', 'name': 'Guam'}, '502': {'code': 'GT', 'name': 'Guatemala'}, '224': {'code': 'GN', 'name': 'Guinea'}, '245': {'code': 'GW', 'name': 'Guinea-Bissau'}, '595': {'code': 'PY', 'name': 'Paraguay'}, '509': {'code': 'HT', 'name': 'Haiti'}, '504': {'code': 'HN', 'name': 'Honduras'}, '36': {'code': 'HU', 'name': 'Hungary'}, '354': {'code': 'IS', 'name': 'Iceland'}, '91': {'code': 'IN', 'name': 'India'}, '62': {'code': 'ID', 'name': 'Indonesia'}, '964': {'code': 'IQ', 'name': 'Iraq'}, '353': {'code': 'IE', 'name': 'Ireland'}, '39': {'code': 'IT', 'name': 'Italy'}, '1 876': {'code': 'JM', 'name': 'Jamaica'}, '81': {'code': 'JP', 'name': 'Japan'}, '962': {'code': 'JO', 'name': 'Jordan'}, '7 7': {'code': 'KZ', 'name': 'Kazakhstan'}, '254': {'code': 'KE', 'name': 'Kenya'}, '686': {'code': 'KI', 'name': 'Kiribati'}, '965': {'code': 'KW', 'name': 'Kuwait'}, '996': {'code': 'KG', 'name': 'Kyrgyzstan'}, '371': {'code': 'LV', 'name': 'Latvia'}, '961': {'code': 'LB', 'name': 'Lebanon'}, '266': {'code': 'LS', 'name': 'Lesotho'}, '231': {'code': 'LR', 'name': 'Liberia'}, '423': {'code': 'LI', 'name': 'Liechtenstein'}, '370': {'code': 'LT', 'name': 'Lithuania'}, '352': {'code': 'LU', 'name': 'Luxembourg'}, '261': {'code': 'MG', 'name': 'Madagascar'}, '265': {'code': 'MW', 'name': 'Malawi'}, '60': {'code': 'MY', 'name': 'Malaysia'}, '960': {'code': 'MV', 'name': 'Maldives'}, '223': {'code': 'ML', 'name': 'Mali'}, '356': {'code': 'MT', 'name': 'Malta'}, '692': {'code': 'MH', 'name': 'Marshall Islands'}, '596': {'code': 'MQ', 'name': 'Martinique'}, '222': {'code': 'MR', 'name': 'Mauritania'}, '230': {'code': 'MU', 'name': 'Mauritius'}, '262': {'code': 'RE', 'name': 'Réunion'}, '52': {'code': 'MX', 'name': 'Mexico'}, '377': {'code': 'MC', 'name': 'Monaco'}, '976': {'code': 'MN', 'name': 'Mongolia'}, '382': {'code': 'ME', 'name': 'Montenegro'}, '1664': {'code': 'MS', 'name': 'Montserrat'}, '212': {'code': 'MA', 'name': 'Morocco'}, '95': {'code': 'MM', 'name': 'Myanmar'}, '264': {'code': 'NA', 'name': 'Namibia'}, '674': {'code': 'NR', 'name': 'Nauru'}, '977': {'code': 'NP', 'name': 'Nepal'}, '31': {'code': 'NL', 'name': 'Netherlands'}, '599': {'code': 'AN', 'name': 'Netherlands Antilles'}, '687': {'code': 'NC', 'name': 'New Caledonia'}, '64': {'code': 'NZ', 'name': 'New Zealand'}, '505': {'code': 'NI', 'name': 'Nicaragua'}, '227': {'code': 'NE', 'name': 'Niger'}, '234': {'code': 'NG', 'name': 'Nigeria'}, '683': {'code': 'NU', 'name': 'Niue'}, '672': {'code': 'NF', 'name': 'Norfolk Island'}, '1 670': {'code': 'MP', 'name': 'Northern Mariana Islands'}, '47': {'code': 'SJ', 'name': 'Svalbard and Jan Mayen'}, '968': {'code': 'OM', 'name': 'Oman'}, '92': {'code': 'PK', 'name': 'Pakistan'}, '680': {'code': 'PW', 'name': 'Palau'}, '507': {'code': 'PA', 'name': 'Panama'}, '675': {'code': 'PG', 'name': 'Papua New Guinea'}, '51': {'code': 'PE', 'name': 'Peru'}, '63': {'code': 'PH', 'name': 'Philippines'}, '48': {'code': 'PL', 'name': 'Poland'}, '351': {'code': 'PT', 'name': 'Portugal'}, '1 939': {'code': 'PR', 'name': 'Puerto Rico'}, '974': {'code': 'QA', 'name': 'Qatar'}, '40': {'code': 'RO', 'name': 'Romania'}, '250': {'code': 'RW', 'name': 'Rwanda'}, '685': {'code': 'WS', 'name': 'Samoa'}, '378': {'code': 'SM', 'name': 'San Marino'}, '966': {'code': 'SA', 'name': 'Saudi Arabia'}, '221': {'code': 'SN', 'name': 'Senegal'}, '381': {'code': 'RS', 'name': 'Serbia'}, '248': {'code': 'SC', 'name': 'Seychelles'}, '232': {'code': 'SL', 'name': 'Sierra Leone'}, '65': {'code': 'SG', 'name': 'Singapore'}, '421': {'code': 'SK', 'name': 'Slovakia'}, '386': {'code': 'SI', 'name': 'Slovenia'}, '677': {'code': 'SB', 'name': 'Solomon Islands'}, '27': {'code': 'ZA', 'name': 'South Africa'}, '500': {'code': 'FK', 'name': 'Falkland Islands (Malvinas)'}, '34': {'code': 'ES', 'name': 'Spain'}, '94': {'code': 'LK', 'name': 'Sri Lanka'}, '249': {'code': 'SD', 'name': 'Sudan'}, '597': {'code': 'SR', 'name': 'Suriname'}, '268': {'code': 'SZ', 'name': 'Swaziland'}, '46': {'code': 'SE', 'name': 'Sweden'}, '41': {'code': 'CH', 'name': 'Switzerland'}, '992': {'code': 'TJ', 'name': 'Tajikistan'}, '66': {'code': 'TH', 'name': 'Thailand'}, '228': {'code': 'TG', 'name': 'Togo'}, '690': {'code': 'TK', 'name': 'Tokelau'}, '676': {'code': 'TO', 'name': 'Tonga'}, '1 868': {'code': 'TT', 'name': 'Trinidad and Tobago'}, '216': {'code': 'TN', 'name': 'Tunisia'}, '90': {'code': 'TR', 'name': 'Turkey'}, '993': {'code': 'TM', 'name': 'Turkmenistan'}, '1 649': {'code': 'TC', 'name': 'Turks and Caicos Islands'}, '688': {'code': 'TV', 'name': 'Tuvalu'}, '256': {'code': 'UG', 'name': 'Uganda'}, '380': {'code': 'UA', 'name': 'Ukraine'}, '971': {'code': 'AE', 'name': 'United Arab Emirates'}, '44': {'code': 'JE', 'name': 'Jersey'}, '598': {'code': 'UY', 'name': 'Uruguay'}, '998': {'code': 'UZ', 'name': 'Uzbekistan'}, '678': {'code': 'VU', 'name': 'Vanuatu'}, '681': {'code': 'WF', 'name': 'Wallis and Futuna'}, '967': {'code': 'YE', 'name': 'Yemen'}, '260': {'code': 'ZM', 'name': 'Zambia'}, '263': {'code': 'ZW', 'name': 'Zimbabwe'}, '': {'code': 'AX', 'name': 'land Islands'}, '591': {'code': 'BO', 'name': 'Bolivia, Plurinational State of'}, '673': {'code': 'BN', 'name': 'Brunei Darussalam'}, '243': {'code': 'CD', 'name': 'Congo, The Democratic Republic of the'}, '225': {'code': 'CI', 'name': "Cote d'Ivoire"}, '379': {'code': 'VA', 'name': 'Holy See (Vatican City State)'}, '852': {'code': 'HK', 'name': 'Hong Kong'}, '98': {'code': 'IR', 'name': 'Iran, Islamic Republic of'}, '850': {'code': 'KP', 'name': "Korea, Democratic People's Republic of"}, '82': {'code': 'KR', 'name': 'Korea, Republic of'}, '856': {'code': 'LA', 'name': "Lao People's Democratic Republic"}, '218': {'code': 'LY', 'name': 'Libyan Arab Jamahiriya'}, '853': {'code': 'MO', 'name': 'Macao'}, '389': {'code': 'MK', 'name': 'Macedonia, The Former Yugoslav Republic of'}, '691': {'code': 'FM', 'name': 'Micronesia, Federated States of'}, '373': {'code': 'MD', 'name': 'Moldova, Republic of'}, '258': {'code': 'MZ', 'name': 'Mozambique'}, '970': {'code': 'PS', 'name': 'Palestinian Territory, Occupied'}, '872': {'code': 'PN', 'name': 'Pitcairn'}, '7': {'code': 'RU', 'name': 'Russia'}, '290': {'code': 'SH', 'name': 'Saint Helena, Ascension and Tristan Da Cunha'}, '1 869': {'code': 'KN', 'name': 'Saint Kitts and Nevis'}, '1 758': {'code': 'LC', 'name': 'Saint Lucia'}, '508': {'code': 'PM', 'name': 'Saint Pierre and Miquelon'}, '1 784': {'code': 'VC', 'name': 'Saint Vincent and the Grenadines'}, '239': {'code': 'ST', 'name': 'Sao Tome and Principe'}, '252': {'code': 'SO', 'name': 'Somalia'}, '963': {'code': 'SY', 'name': 'Syrian Arab Republic'}, '886': {'code': 'TW', 'name': 'Taiwan, Province of China'}, '255': {'code': 'TZ', 'name': 'Tanzania, United Republic of'}, '670': {'code': 'TL', 'name': 'Timor-Leste'}, '58': {'code': 'VE', 'name': 'Venezuela, Bolivarian Republic of'}, '84': {'code': 'VN', 'name': 'Viet Nam'}, '1 284': {'code': 'VG', 'name': 'Virgin Islands, British'}, '1 340': {'code': 'VI', 'name': 'Virgin Islands, U.S.'}}
      }
  },
  methods: {
    emitValue() {
      this.$emit('input', '+' + this.code + ' ' + this.phone)
    }
  }
}
</script>

<style scoped>

input:-moz-placeholder, textarea:-moz-placeholder { color: #000000 !important; }
input:-ms-input-placeholder, textarea:-ms-input-placeholder { color: #000000 !important; }
input::-webkit-input-placeholder, textarea::-webkit-input-placeholder { color: #000000 !important; }

</style>
