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
      // 100% 透明度
      '#ffffff',
      '#000000',
      '#ff0000',
      '#ff4500',
      '#ff8c00',
      '#ffd700',
      '#90ee90',
      '#00ced1',
      '#1e90ff',
      '#c71585',

      // 25% 透明度
      'rgba(255,255,255,0.25)',
      'rgba(0,0,0,0.25)',
      'rgba(255,0,0,0.25)',
      'rgba(255,69,0,0.25)',
      'rgba(255,140,0,0.25)',
      'rgba(255,215,0,0.25)',
      'rgba(144,238,144,0.25)',
      'rgba(0,206,209,0.25)',
      'rgba(30,144,255,0.25)',
      'rgba(199,21,133,0.25)',

      // 50% 透明度
      'rgba(255,255,255,0.50)',
      'rgba(0,0,0,0.50)',
      'rgba(255,0,0,0.50)',
      'rgba(255,69,0,0.50)',
      'rgba(255,140,0,0.50)',
      'rgba(255,215,0,0.50)',
      'rgba(144,238,144,0.50)',
      'rgba(0,206,209,0.50)',
      'rgba(30,144,255,0.50)',
      'rgba(199,21,133,0.50)',

      // 75% 透明度
      'rgba(255,255,255,0.75)',
      'rgba(0,0,0,0.75)',
      'rgba(255,0,0,0.75)',
      'rgba(255,69,0,0.75)',
      'rgba(255,140,0,0.75)',
      'rgba(255,215,0,0.75)',
      'rgba(144,238,144,0.75)',
      'rgba(0,206,209,0.75)',
      'rgba(30,144,255,0.75)',
      'rgba(199,21,133,0.75)',
    ]);

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
