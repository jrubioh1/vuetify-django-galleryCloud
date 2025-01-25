<template>
  <v-container class="my-5 text-center">
    <span class="text-h5">{{ $t('title_staistics1') }}</span>
    <sunburst 
      v-if="staistics" 
      :data="staistics"
    />
  </v-container>
 
  <v-container v-if="!staistics">
    {{ $t('noData') }}
  </v-container>
</template>
<script setup>
import sunburst from '@/components/echartSunburts.vue'
import { onMounted } from 'vue';
import { useAppStore } from '@/stores/app';
import { storeToRefs } from 'pinia';
const {staistics}=storeToRefs(useAppStore())


onMounted(async()=>{
  useAppStore().get_satistics()
})

</script>