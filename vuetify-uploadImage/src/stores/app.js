// Utilities
import { defineStore } from 'pinia'
import {axiosWrapper} from '@/helpers/axiosWrapper.js'

export const useAppStore = defineStore('app', {
  state: () => ({
    api:import.meta.env.VITE_API_URL,
    loading:false,
    selectableDate:null,
    selectedYear: null,
    selectedMonth: null,
    previous:null, 
    next:null,
    images:null,
    staistics:null,
    language:'en'
    //
  }),
  actions:{
    setLanguage(lang) {
      this.language = lang; // Actualiza el idioma
    },
    async  get_images_by_year_month() {
      this.loading=true
      try {
        const params = new URLSearchParams();
        if (this.selectedYear) params.append('year', this.selectedYear);
        if (this.selectedMonth) params.append('month',this.selectedMonth);
        const response = await axiosWrapper.get(this.api + 'uploads/get_images_by_year_month/', {params})
        if(Object.keys(response.data.results).length!=0){
          // console.log(response.data.results)
          await this.get_available_years_and_months()
          this.images = response.data.results 
          this.previous=response.data.previous
          this.next=response.data.next
        }else{this.images=null}
        
      } catch (error) {
        this.images={}
        console.log(error)
      }finally {
        this.loading = false;
      }
    },async get_next_or_previous_page(url) {
      
      try{const response = await axiosWrapper.get(url);
      const newImages = response.data.results;
    
      // Agregar nuevas imágenes a las existentes
      Object.entries(newImages).forEach(([year, months]) => {
        if (!this.images[year]) {
          this.images[year] = {};
        }
        Object.entries(months).forEach(([month, images]) => {
          if (!this.images[year][month]) {
            this.images[year][month] = [];
          }
          this.images[year][month].push(...images);
        });
      });
      
      this.next = response.data.next;
      this.previous = response.data.previous;
    }catch(e){
      console.log(e)
    }
      
    },
    
    async get_available_years_and_months() {
      try {
        this.selectableDate=null
        const response = await axiosWrapper.get(this.api + 'uploads/get_available_years_and_months/')
        this.selectableDate=response.data
       
        
      } catch (error) {
        console.log(error)
      }
    },
    async get_satistics(){
      this.staistics=null
      try{
        const response= await axiosWrapper.get(this.api+'uploads/photos_tree_staistics/')
        if(response.data.length!=0)this.staistics=response.data
      }
      catch(e){
        console.log(e)
      }
    }

    
  }
  
})
