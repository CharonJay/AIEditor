<template>
    <el-table :data="files" class ="table" :row-style="{ height: '5rem', 'font-size':'1.2rem' }" :cell-style="{ padding: '0px', 'font-size': '1.2rem' }">
        <el-table-column prop="name" label="文件名">
            <template #default="{ row }">
                <el-icon size="32"><Document /></el-icon>
                &nbsp;&nbsp;{{ row.name }}
            </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="上次更新">
            <template #default="{ row }">
                {{ new Date(row.updated_at).toLocaleDateString() }}
            </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建者"></el-table-column>
        <el-table-column fixed="right" label="操作" min-width="120px" align="center" width="200px">
            <template #default="{ row }" >
                <el-button link @click="handleDelete(row.id, false)" type="primary" size="large" style="width: 50px;">恢复</el-button>
                <el-button link @click="handleDelete(row.id, true)" type="primary" size="large" style="width: 50px;">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
</template>

<script setup name="CreateComponent">
    import { ref, onMounted } from 'vue'
    import axios from 'axios';

    const files = ref([])

    const handleDelete = async(index, flag) => {
        if (flag) {
            console.log(index)
            await axios.delete(`/api/user/files/deletefile/${index}/`)
            const response = await fetch('/api/user/filesMenu/trash/'+localStorage.getItem('username')+'/')
            const data = await response.json()
            files.value = data
        }else {
            await axios.patch(`/api/user/files/updatefile/${index}/`,{
                status: 0
            })
            const response = await fetch('/api/user/filesMenu/trash/'+localStorage.getItem('username')+'/')
            const data = await response.json()
            files.value = data
        }
    }

    onMounted(async () => {
        const response = await fetch('/api/user/filesMenu/trash/'+localStorage.getItem('username')+'/')
        const data = await response.json()
        files.value = data
    })

</script>

<style scoped>
.table {
    line-height: 60px;
    font-size: 1.2rem;
    font-weight: bolder;
    margin: 1.1rem 0;
    letter-spacing: 0.1rem;
    font-family: sans-serif;
    border-radius: 10px;
}
a {
    color: #333;
    font-size: 1.2rem;
    text-decoration: none;
}
</style>