<template>
    <div>
        <div class="row">
            <div class="col-md-4">
                <strong>Notes</strong>
                <p class="text-instructions">
                    To add a note - type your note in the Note Box and hit the "Submit Note"
                    button.
                </p>
            </div>
            <div class="col-md-8">
                <label>Note Box</label>
                <editor
                    :init="{
                        height: 250,
                        menubar: false,
                        plugins: ['lists','table'],
                        toolbar: [
                           'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                           'bold italic strikethrough underline backcolor | table | ' +
                           'bullist numlist outdent indent | removeformat'
                        ]}"
                    v-bind:content_css="false"
                    v-bind:skin="false"
                    v-model="cardNoteModel"
                />
            </div>
        </div>
        <hr>
        <div class="row">
            <div class="col-md-12">
                <button class="btn btn-secondary"
                        v-on:click="closeModal"
                >
                    Close
                </button>
                <button class="btn btn-primary save-changes"
                        v-on:click="addNote"
                        v-bind:disabled="cardNoteModel===''"
                >
                    Add Note
                </button>
            </div>
        </div>
        <hr>

        <!-- NOTE HISTORY -->
        <list-notes v-bind:note-history-results="cardNotes"
                    v-bind:destination="'card'"
        ></list-notes>
    </div>
</template>

<script>
    const axios = require('axios');
    import Editor from '@tinymce/tinymce-vue'
    import ListNotes from "../modules/sub_modules/ListNotes.vue";

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: 'CardNotes',
        components: {
            'editor': Editor,
            ListNotes,
        },
        props: {},
        data() {
            return {
                // ...mapGetters(['getCardNotes']),
                cardNoteModel: '',
            }
        },
        computed: {
            ...mapGetters({
                cardNotes: "getCardNotes",
                rootUrl: "getRootUrl",
            })
        },
        methods: {
            addNote: function() {
                //Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('note',this.cardNoteModel);

                //Use axios to send the data
                axios.post(
                    `${this.rootUrl}object_data/kanban_card/${this.$store.state.card.cardId}/add_notes/`,
                    data_to_send,
                ).then(response => {
                    //Add the response to the end of the noteHistoryResults
                    this.$store.commit({
                        type: 'appendNote',
                        newNote: response['data'][0],
                    });

                    //Clear the card note model
                    this.cardNoteModel = '';
                }).catch(error => {
                    
                });
            },
            closeModal: function() {
                document.getElementById("cardInformationModalCloseButton").click();
            },
        },
    }
</script>

