class Janela {
    constructor() {
        if (this.constructor === Janela) {
            throw new Error('A classe "Janela" não pode ser instanciada diretamente.');
        }
    }
    static checkNotThisClass() {
        if (this.constructor === Janela) throw new Error("Cannot instantiate abstract class Janela directly.");
    }
    static beforeOpen() {this.checkNotThisClass();}
    static afterOpen() {this.checkNotThisClass();}
    static beforeClose() {this.checkNotThisClass();}
    static afterClose() {this.checkNotThisClass();}
}

export default Janela;