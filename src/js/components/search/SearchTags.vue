<template xmlns:v-bind="http://www.w3.org/1999/xhtml">
    <div class="card">
        <div class="card-body">
            <h1>Search Tags</h1>
            <hr>
            
            <div class="row">
                <div class="col-md-4">
                    <strong>Tags</strong>
                    <p class="text-instructions">
                        Use the search bar to help you find any tags.
                    </p>

                    <p class="text-instructions">
                        Click on the icon <Icon v-bind:icon="icons.infoCircle"></Icon>
                        to edit the tag.
                    </p>

                    <p class="text-instructions">
                        To add in any new tags - please click on the "New Tag" button.
                    </p>
                </div>

                <div class="col-md-8 tag-list">
                    <div v-for="tag in localTagResults"
                         v-bind:key="tag['pk']" 
                         v-bind:style="`background-color: ${tag['fields']['tag_colour']};`"
                         v-on:dblclick="editTag(tag['pk'])"
                         class="single-tag"
                    >
                        {{tag['fields']['tag_name']}}
                        <span v-on:click="editTag(tag['pk'])"
                        >
                            <Icon v-bind:icon="icons.infoCircle"></Icon>
                        </span>
                    </div>
                </div>

                <!-- ADD NEW TAG BUTTON -->
                <hr>
                <div class="row submit-row">
                    <div class="col-md-12">
                        <a href="javascript:void(0)"
                           class="btn btn-primary save-changes"
                           v-on:click="addTag"
                        >Add Tag</a>
                    </div>
                </div>
            </div>

            <!-- MODALS -->
            <edit-tag-modal v-bind:existing-tags="localTagResults"
                            v-bind:tag-colour="singleTagColour"
                            v-bind:tag-id="singleTagId"
                            v-bind:tag-name="singleTagName"
                            v-on:new_tag="newTag"
                            v-on:delete_tag="deleteTag($event)"
                            v-on:update_tags="updateTags"
            ></edit-tag-modal>
        </div>
    </div>
</template>

<script>
    //MIXINS
    import iconMixin from '../../mixins/iconMixin';
    import { Modal } from 'bootstrap';
    import { Icon } from '@iconify/vue';
    import EditTagModal from "../tags/EditTagModal.vue";

    export default {
        name: 'SearchTags',
        components: {
            EditTagModal,
            Icon,
        },
        props: {
            rootUrl: {
                type: String,
                default: '/',
            },
            tagResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        data() {
            return {
                /*singleTag: {
                    tagName: '',
                    tagColour: '',
                },*/
                singleTagColour: '',
                singleTagId: 0,
                singleTagName: '',
                localTagResults: this.tagResults,
            }
        },
        mixins: [
            iconMixin
        ],
        methods: {
            addTag: function() {
                //Send data down to the modal
                this.singleTagName = 'default tag';
                this.singleTagId = 0;
                this.singleTagColour = '#37cbd2';

                //Open up modal
                let edit_tag_modal = new Modal(document.getElementById('editTagModal'));
                edit_tag_modal.show();
            },
            deleteTag: function(data) {
                //Filter out the tag
                this.localTagResults = this.localTagResults.filter(row => {
                    return row['pk'] !== data['tag_id'];
                })
            },
            editTag: function(tag_id) {
                //Filter for the tag information
                let single_tag = this.localTagResults.filter(row => {
                    return row['pk'] == tag_id;
                })[0];

                //Send data down to the modal
                this.singleTagName = single_tag['fields']['tag_name'];
                this.singleTagId = tag_id;
                this.singleTagColour = single_tag['fields']['tag_colour'];

                //Open up modal
                let edit_tag_modal = new Modal(document.getElementById('editTagModal'));
                edit_tag_modal.show();
            },
            newTag: function(data) {
                
                this.localTagResults.push(data[0]);
            },
            updateTags: function(data) {
                //Get the index location of the object we are updating
                let index = this.localTagResults.findIndex( row => {
                    return row['pk'] === data['tag_id'];
                });

                // Update the data
                this.localTagResults[index]['fields']['tag_name'] = data['tag_name'];
                this.localTagResults[index]['fields']['tag_colour'] = data['tag_colour'];
            }
        },
        mounted() {
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
            });
        }
    }
</script>
