<template>
  <v-container>
    <div
      ref="chartDom"
      :style=" `height: ${props.height}px; width: auto;`"
    />
  </v-container>
</template>
<script setup>
import * as echarts from 'echarts';
import { onMounted } from 'vue';
import {ref, computed} from 'vue'

const props= defineProps(
    {
        height:{
            type: Number,
            required:false,
            default:600
        },
        data:{
            type:Object,
            required:true
        },
      
    }

)
var chartDom =ref(null)
var myChart =null



 const option = computed(()=>({
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c}' // {b} muestra el nombre del nodo, {c} el valor asociado
  },
  visualMap: {
    type: 'continuous',
    min: 0,
    max: 10,
    inRange: {
      color: ['#2F93C8', '#AEC48F', '#FFDB5C', '#F98862']
    }
  },
  series: {
    type: 'sunburst',
    data: props.data,
    radius: [0, '90%'],
    label: {
      rotate: 'radial'
    },
    
  }
 }))
 onMounted(()=>{
    myChart = echarts.init(chartDom.value);
    myChart.setOption(option.value);
    

 })


</script>