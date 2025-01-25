<template>
  <v-container
    v-if="images"
    class="my-5"
  >
    <v-speed-dial
      v-if="images && !isMobile"
      style="position: fixed; z-index: 9999;"
      class="pa-2" 
    >
      <template #activator="{ props: activatorProps }">
        <v-fab
          v-bind="activatorProps"
          color="blue-grey-lighten-4"
          size="large"
          icon="mdi-menu"
          style="position: fixed; top: 85%; right: 8%; z-index: 9999;"
        />
      </template>

      <v-btn
        v-if="selected.length > 0"
        key="1"
        prepend-icon="mdi-delete"
        @click="delete_selected(selected, api); selected=[]"
      >
        {{ t('imagespage.deleteSelected') }}
      </v-btn>
      <v-btn
        key="2"
        prepend-icon="mdi-refresh"
        @click="useAppStore().get_images_by_year_month(); selected=[]"
      >
        {{ t('imagespage.refresh') }}
      </v-btn>
      <v-btn
        key="3"
        prepend-icon="mdi-select-all"
        @click="selected = select_all(images)"
      >
        {{ t('imagespage.selectAll') }}
      </v-btn>
      <v-btn
        v-if="selected.length > 0"
        key="4"
        prepend-icon="mdi-select-off"
        @click="selected = []"
      >
        {{ t('imagespage.deselectAll') }}
      </v-btn>
      <v-btn
        v-if="selected.length > 0"
        key="5"
        prepend-icon="mdi-download"
        @click="download_selected(selected, api); selected=[]"
      >
        {{ t('imagespage.downloadSelected') }}
      </v-btn>
    </v-speed-dial>
    <v-speed-dial
      v-if="images && isMobile"
      style="position: fixed; z-index: 9999;"
      class="pa-2" 
    >
      <template #activator="{ props: activatorProps }">
        <v-fab
          v-bind="activatorProps"
          color="blue-grey-lighten-4"
          size="large"
          icon="mdi-menu"
          style="position: fixed; top: 4%; right: 55%; z-index: 9999;"
        />
      </template>

      <v-btn
        v-if="selected.length > 0"
        key="1"
        prepend-icon="mdi-delete"
        @click="delete_selected(selected, api); selected=[]"
      >
        {{ t('imagespage.deleteSelected') }}
      </v-btn>
      <v-btn
        key="2"
        prepend-icon="mdi-refresh"
        @click="useAppStore().get_images_by_year_month(); selected=[]"
      >
        {{ t('imagespage.refresh') }}
      </v-btn>
      <v-btn
        key="3"
        prepend-icon="mdi-select-all"
        @click="selected = select_all(images)"
      >
        {{ t('imagespage.selectAll') }}
      </v-btn>
      <v-btn
        v-if="selected.length > 0"
        key="4"
        prepend-icon="mdi-select-off"
        @click="selected = []"
      >
        {{ t('imagespage.deselectAll') }}
      </v-btn>
      <v-btn
        v-if="selected.length > 0"
        key="5"
        prepend-icon="mdi-download"
        @click="download_selected(selected, api); selected=[]"
      >
        {{ t('imagespage.downloadSelected') }}
      </v-btn>
    </v-speed-dial>

    <v-bottom-navigation
      v-if="images"
      style="position: fixed;"
    >
      <v-select
        v-if="selectableDate"
        v-model="selectedYear"
        class="bg-blue-grey-lighten-4"
        clearable
        :label="t('imagespage.filterYear')"
        :items="Object.keys(selectableDate)"
      />
      <v-select
        v-if="selectedYear && selectableDate"
        v-model="selectedMonth"
        class="bg-blue-grey-lighten-4"
        clearable
        :label="t('imagespage.filterMonth')"
        :items="selectableDate[selectedYear].map((month) => month)"
      />
    </v-bottom-navigation>

    <v-row
      v-for="[year, month] in Object.entries(images).sort(([yearA], [yearB]) => yearB - yearA)"
      :key="year"
    >
      <v-container
        v-for="[month_, images_] in Object.entries(month)
          .sort(([monthA], [monthB]) => monthB - monthA)"
        :key="month_"
        class="pa-3"
      >
        <v-row class="d-flex flex-row my-3">
          <v-col
            class="d-flex flex-column alig-center text-center"
            cols="12"
            sm="6"
            md="4"
          >
            <span class="text-h6">{{ `${month_} ${year}` }}</span>
          </v-col><v-divider class="my-3" />
         

          <v-row class="d-flex flex-row">
            <v-col
              
              v-for="image in images_"
              :key="image.id"
              cols="12"
              lg="2"
              md="3"
              sm="6"
              xs="12"
            >
              <v-card
                class="d-flex flex-column align-center"
                elevation="0"
              >
                <v-responsive>
                  <v-checkbox
                    v-model="selected"
                    class="d-flex flex-lg-column align-center"
                    :value="image.id"
                    density="compact"
                  />
                  <v-img
                    :src="image.url"
                    class="rounded-lg mb-2"
                  />
                  <v-card-text class="text-center">
                    <span>{{ image.name }}</span>
                    <br>
                    <small>{{ format(parseISO(image.uploaded_at), 'dd/MM/yyyy HH:mm:ss') }}</small>
                  </v-card-text>

                  <v-card-actions class="d-flex justify-center">
                    <v-btn
                      icon
                      color="error"
                      @click="delete_image(image.id, api)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      color="primary"
                      @click="download_image(image.id, api)"
                    >
                      <v-icon>mdi-download</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-responsive>  
              </v-card>
            </v-col>
          </v-row>
        </v-row>
      </v-container>
    </v-row>
    <div
      v-if="next"
      class="text-center"  
    >
      <v-progress-circular
        color="primary"
        indeterminate
      />
    </div>
  </v-container>
  <v-container v-if="!images">
    {{ t('imagespage.noImages') }}
  </v-container>
</template>
<script setup>
import debounce from 'lodash/debounce';
import { format, parseISO } from 'date-fns'
import { watch} from 'vue';
import { onMounted, onUnmounted } from 'vue';
import { ref,computed } from 'vue'
import { storeToRefs } from 'pinia';
import { useAppStore } from '@/stores/app';
import {download_image, download_selected, delete_selected ,delete_image, select_all} from '@/helpers/helpers_images.js'
import {useI18n} from 'vue-i18n'
const{t}=useI18n()

const {api, images, selectedMonth, selectableDate,selectedYear,  next}=storeToRefs(useAppStore())
const selected = ref([])
import { useDisplay } from 'vuetify';
import { se } from 'date-fns/locale';
const{xs} =useDisplay()
const isMobile=computed(()=>xs.value)

// el debounce hace que no se ejecute el evento hasta que no haya pasado x ms desde que termina el evento, para mejorar la eficiencia
const handleScroll = debounce(() => {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight;
  const clientHeight = window.innerHeight || document.documentElement.clientHeight;

  if (scrollTop + clientHeight >= scrollHeight - 200 && next.value) {
    useAppStore().get_next_or_previous_page(next.value);
  }
}, 200);
const scrollTop=()=>{
  window.scrollTo({
    top: 0,
    behavior: 'smooth', // Para un desplazamiento suave
  });
}
onMounted(() => {
  useAppStore().get_images_by_year_month()
  window.addEventListener('scroll', handleScroll);
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});


watch(selectedYear, () => {
  if (!selectedYear.value) {
    selectedMonth.value = null
  }
  useAppStore().get_images_by_year_month()
  scrollTop()
})
watch(selectedMonth, () => {
  useAppStore().get_images_by_year_month()
  scrollTop()
})


</script>
<style scoped>
</style>