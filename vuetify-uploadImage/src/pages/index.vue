<template>
  <v-container v-if="files">
    <v-row class="d-flex flex-row align-center">
      <v-col class="d-flex flex-column align-center">
        <v-btn
          :text="t('upload')"
          width="100%"
          :disabled="files.length == 0"
          @click="upload_images"
        />
      </v-col>
    </v-row>
  </v-container>
  <v-container>
    <v-file-upload
      :key="key"
      v-model="files"
      density="comfortable"
      variant="comfortable"
      accept="image/*"
      clearable
      multiple
      :title="t('fileUpload.defaultText')"
    />
  </v-container>
</template>

<script setup>
import { VFileUpload } from 'vuetify/labs/VFileUpload'
import {axiosWrapper} from '@/helpers/axiosWrapper.js'
import { ref } from 'vue'
import { watch } from 'vue';
import { useAppStore } from '@/stores/app';
import { storeToRefs } from 'pinia';
import {useI18n} from 'vue-i18n'
const{t}=useI18n()

const files = ref([])
const key = ref(0)
const {api}=storeToRefs(useAppStore())

async function upload_images() {
  
  if (files.value.length == 0) { alert(t('selectImages')) } 
  else if(files.value.length>1000){alert(t('tooManyFiles'))}
  else {
    try {
      const formData = new FormData()
      console.log(files.value)
      files.value.forEach((file) => {
        formData.append('image', file);
      });
      const response = await axiosWrapper.post(api.value+'uploads/upload_image/', formData,  'multipart/form-data' )
      alert(t('uploadSuccess'), response.data)
      files.value = []

    } catch (e) {
      alert(t('uploadError'), e.response)
      console.error(e)
    }
  }


}

watch(files, () => {
  files.value.length == 0 ? key.value++ : ""
})

</script>
