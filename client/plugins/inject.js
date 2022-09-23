import Vue from 'vue';

export default ({app}, inject) => {
    inject('set', (object, key, value) => {
        Vue.$set(object, key, value);
    });

    inject('delete', (object, key) => {
        Vue.$delete(object, key);
    });
}
