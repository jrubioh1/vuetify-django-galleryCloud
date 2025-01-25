<template>
  <v-app :theme="theme">
    <Header @click="onClick" :theme="theme"/>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import Header from './Header.vue';
import { ref } from 'vue'

const theme = ref('light')

function onClick() {
   theme.value = theme.value === 'light' ? 'dark' : 'light'
}
//
</script>
