<template>
  <el-color-picker
      v-model="color"
      @change="updateColor"
      class="color-picker"
      show-alpha
      :title="title"
      :predefine="predefineColors"
  >
  </el-color-picker>
</template>


<script>
import {ref} from "vue";


export default {
  name: 'MenuColorItem',
  props: {
    icon: {
      type: String,
      default: 'font-color'
    },
    title: {
      type: String,
      required: true
    },
    initialColor: {
      type: String,
      default: '#000000'
    },
    onChange: {
      type: Function,
      required: true
    },
  },
  setup() {
    const predefineColors = ref([
      '#ff4500',
      '#ff8c00',
      '#ffd700',
      '#90ee90',
      '#00ced1',
      '#1e90ff',
      '#c71585',
      'rgba(255, 69, 0, 0.68)',
      'rgb(255, 120, 0)',
      'hsv(51, 100, 98)',
      'hsva(120, 40, 94, 0.5)',
      'hsl(181, 100%, 37%)',
      'hsla(209, 100%, 56%, 0.73)',
      '#c7158577',
    ])
    return {
      predefineColors
    }
  },
  data() {
    return {
      color: this.initialColor,
    };
  },
  methods: {
    updateColor(color) {
      this.color = color;
      this.onChange(color);
    }
  }
};
</script>

<style lang="scss">
.color-picker {
  border: none;
  background: none;
  cursor: pointer;
}

.color-picker .el-color-picker__trigger{
  border: none;
  height: 1.8rem;
  width: 1.8rem;
  top: 0.1rem;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin-right: 0.2rem;
}


</style>
