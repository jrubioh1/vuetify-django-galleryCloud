<template>
  <v-app-bar
    style="position: fixed;"
    color="blue-grey-lighten-4"
  >
    <v-toolbar-title> {{ t('title_app') }}</v-toolbar-title>
    <v-spacer />
    <v-btn
      v-if="!isMobile"
      text
      to="/"
    >
      {{ t('upload') }}
    </v-btn>
    <v-btn
      v-if="!isMobile"
      text
      to="images"
    >
      {{ t('images') }}
    </v-btn>
    <v-btn
      v-if="!isMobile"
      text
      to="staistics"
    >
      {{ t('staistics') }}
    </v-btn>
    <v-btn
      v-if="!isMobile"
      :prepend-icon="icon"
      slim
      @click="onClick"
    />
    <v-menu
      v-if="!isMobile"
    >
      <template #activator="{ props }">
        <v-btn
          text
          v-bind="props"
          prepend-icon="mdi-translate"
        >
          {{ currentLanguageText }}
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="lang in languages"
          :key="lang.value"
          @click="changeLanguage(lang.value)"
        >
          <v-list-item-title>{{ lang.text }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-btn
      v-show="isMobile"
      icon
      @click="drawer = !drawer"
    >
      <v-icon>mdi-menu</v-icon>
    </v-btn>
  </v-app-bar>
  <!-- Navigation Drawer -->
  <v-navigation-drawer
    v-model="drawer"
    mobile-breakpoint="sm"
    temporary
    style="position: fixed;"
    class="overflow-y-auto h-100"
    color="blue-grey-lighten-4"
  >
    <v-row class="ma-1">
      <v-col cols="6">
        <v-menu>
          <template #activator="{ props }">
            <v-btn
              color="blue-grey-lighten-4"
              elevation="0"
              text
              v-bind="props"
              prepend-icon="mdi-translate"
            >
              {{ currentLanguageText }}
            </v-btn>
          </template>

          <v-list class="bg-blue-grey-lighten-4">
            <v-list-item
              v-for="lang in languages"
              :key="lang.value"
              @click="changeLanguage(lang.value)"
            >
              <v-list-item-title>{{ lang.text }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
      <v-col cols="6">
        <v-btn
          color="blue-grey-lighten-4"
          elevation="0"
          :prepend-icon="icon"
          slim
          @click="onClick"
        />
      </v-col>
    </v-row>
    <v-list>
      <v-list-item
        to="/"
      >
        <v-list-item-title>{{ t('upload') }}</v-list-item-title>
      </v-list-item>
      <v-list-item
        to="images"
      >
        <v-list-item-title>{{ t('images') }}</v-list-item-title>
      </v-list-item>
      <v-list-item
        to="staistics"
      >
        <v-list-item-title>{{ t('staistics') }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
<script setup>
import {  computed, ref  } from 'vue'
import {useI18n} from 'vue-i18n'
import { useDisplay } from 'vuetify'
import { useAppStore } from '@/stores/app'
import { useRoute } from 'vue-router'

const{t}=useI18n()
const props = defineProps({ theme: { type: String, default: 'light' } })
const icon =computed(() => props.theme === 'light' ? 'mdi-weather-night' : 'mdi-weather-sunny')
const emit = defineEmits(['click'])
const{smAndDown}=useDisplay()
const isMobile=computed(()=>smAndDown.value)
const drawer = ref(false);
const router=useRoute()
const languages = [
  { text: 'English', value: 'en' },
  { text: 'Español', value: 'es' },
];
const { locale } = useI18n(); // Acceso al idioma actual
function onClick () {
    emit('click')
  }




// Idioma seleccionado actualmente
const currentLanguageText = computed(() => {
  const currentLang = languages.find((lang) => lang.value === locale.value);
  return currentLang ? currentLang.text : 'Language';
});

// Cambiar idioma
const changeLanguage = (lang) => {
  locale.value = lang; // Actualiza el idioma en Vue I18n
  useAppStore().setLanguage(lang)
  console.log(router.name)
  if(router.name=='/images')useAppStore().get_images_by_year_month()
  if(router.name=='/staistics')useAppStore().get_satistics()
  
  


};

  
</script>