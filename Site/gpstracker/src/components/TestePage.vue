<template>
  <div class="hello">
    <input v-model="mensagem" @keyup.enter="enviar" placeholder="Digite algo...">
    <p v-for="(msg, i) in mensagens" :key="i">{{ msg }}</p>
  </div>
</template>

<script>
export default {
    
    data() {
        return {           
            ws: null,
            mensagem: '',
            mensagens: []
        };
    },
    mounted() {
        
        this.ws = new WebSocket("ws://10.8.0.18:8765");

        this.ws.onopen = () => {
            console.log("WebSocket conectado");
        };

        this.ws.onmessage = (event) => {
            this.receber(event.data);
        };

        this.ws.onclose = () => {
            console.log("WebSocket desconectado");
        };
    },
    
    methods: {
        enviar() {
            if (this.mensagem.trim()) {
                this.ws.send(this.mensagem);
                this.mensagens.push(`[->] ${this.mensagem}`);
                this.mensagem = '';
            }
        },
        receber(msg) {
            this.mensagens.push(`[<-] ${msg}`);
        }
    }

}


</script>
