<template>
    <div class="modal fade"
         id="newLinkModal"
         tabindex="-1"
         aria-labelledby="kanbanLinkModal"
         aria-hidden="true"
         v-bind:data-kanban-level="levelResults[0]['pk']"
         v-bind:data-kanban-column="columnResults[0]['pk']"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><Icon v-bind:icon="icons.linkOut"></Icon> New Kanban Link Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="requirementLinkCloseButton"
                    >
                        <span aria-hidden="true"></span>
                    </button>
                </div>
                <div class="modal-body">
                    <!-- CHOOSING A OBJECT TYPE -->
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Object Selector</strong>
                            <p class="text-instructions">
                                Please select which object you would like to link to this requirement.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <n-select :options="objectSelection"
                                      v-model:value="objectModel"
                                      class="object-selection"
                                      v-if="!isSearching"
                            ></n-select>
                            <div v-else
                                 class="alert alert-success"
                            >
                                Searching for {{objectModel}}s
                            </div>
                        </div>
                    </div>
                    <hr>

                    <!-- SELECTING WHICH OBJECTS TO LINK TO -->
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Select Links</strong>
                            <p class="text-instructions">
                                Please select which of the objects you want to connect to this requirement.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <!-- LOADING PLACEHOLDER -->
                            <div id="link_wizard_results"
                                 v-if="isSearching || objectModel == null"
                            >
                                <img v-bind:src="`${staticUrl}/NearBeach/images/placeholder/search.svg`"
                                     alt="Searching..."
                                />
                            </div>

                            <div v-if="objectResults.length == 0 && objectModel != null"
                                 class="alert alert-warning"
                            >
                                Sorry - there are no results.
                            </div>

                            <!-- TABLE CONTAINING RESULTS -->
                            <table class="table"
                                   v-if="!isSearching && objectResults.length > 0 && objectModel != null"
                            >
                                <thead>
                                    <tr>
                                        <td>{{objectModel}} Description</td>
                                        <td>Status</td>
                                    </tr>
                                </thead>

                                <!-- PROJECTS -->
                                <tbody v-if="objectModel == 'Project'">
                                    <tr v-for="result in objectResults">
                                        <td>
                                            <div class="form-check">
                                                <input class="form-check-input"
                                                       type="radio"
                                                       name="link-option"
                                                       v-bind:value="result['pk']"
                                                       v-bind:id="`radio_project_${result['pk']}`"
                                                       v-model="linkModel"
                                                >
                                                <label class="form-check-label"
                                                       v-bind:for="`radio_project_${result['pk']}`"
                                                >
                                                    {{result['fields']['project_name']}}
                                                </label>
                                            </div>
                                            <div class="spacer"></div>
                                            <p class="small-text">Project {{result['pk']}}</p>
                                        </td>
                                        <td>{{result['fields']['project_status']}}</td>
                                    </tr>
                                </tbody>

                                <!-- REQUIREMENTS -->
                                <tbody v-if="objectModel == 'Requirement'">
                                    <tr v-for="result in objectResults">
                                        <td>
                                            <div class="form-check">
                                                <input class="form-check-input"
                                                       type="radio"
                                                       name="link-option"
                                                       v-bind:value="result['pk']"
                                                       v-bind:id="`radio_requirement_${result['pk']}`"
                                                       v-model="linkModel"
                                                >
                                                <label class="form-check-label"
                                                       v-bind:for="`radio_task_${result['pk']}`"
                                                >
                                                    {{result['fields']['requirement_title']}}
                                                </label>
                                            </div>
                                            <div class="spacer"></div>
                                            <p class="small-text">Requirement {{result['pk']}}</p>
                                        </td>
                                        <td>{{result['fields']['requirement_status']}}</td>
                                    </tr>
                                </tbody>

                                <!-- TASKS -->
                                <tbody v-if="objectModel == 'Task'">
                                    <tr v-for="result in objectResults">
                                        <td>
                                            <div class="form-check">
                                                <input class="form-check-input"
                                                       type="radio"
                                                       v-bind:value="result['pk']"
                                                       v-bind:id="`radio_task_${result['pk']}`"
                                                       v-model="linkModel"
                                                >
                                                <label class="form-check-label"
                                                       v-bind:for="`radio_task_${result['pk']}`"
                                                >
                                                    {{result['fields']['task_short_description']}}
                                                </label>
                                            </div>
                                            <div class="spacer"></div>
                                            <p class="small-text">Task {{result['pk']}}</p>
                                        </td>
                                        <td>{{result['fields']['task_status']}}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                    >
                        Close
                    </button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:disabled="linkModel.length==0"
                            v-on:click="saveLinks"
                    >Save changes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { Icon } from '@iconify/vue';
    import { NSelect } from 'naive-ui';

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";
    import errorModalMixin from "../../../mixins/errorModalMixin";

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "NewKanbanLinkWizard",
        components: {
            Icon,
            NSelect,
        },
        props: {
            columnResults: {
                type: Array,
                default: () => {
                    return [];
                }
            },
            levelResults: {
                type: Array,
                default: () => {
                    return [];
                }
            },
            locationId: {
                type: Number,
                default: 0,
            },
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
        },
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                isSearching: false,
                objectModel: null,
                objectResults: [],
                objectSelection: [
                    {
                        value: 'Project',
                        label: 'Project',
                    }, {
                        value: 'Requirement',
                        label: 'Requirement',
                    }, {
                        value: 'Task',
                        label: 'Task',
                    },
                ],
                linkModel: [],
            }
        },
        methods: {
            saveLinks: function() {
                // Set up the data object to send
                const data_to_send = new FormData();

                
                //Get the modal to extract data from
                var self_modal = document.getElementById('newLinkModal');

                //Depending on what the object model is - depends what is sent
                data_to_send.set(`${this.objectModel.toLowerCase()}`,this.linkModel);
                data_to_send.set('kanban_level',self_modal['dataset']['kanbanLevel']);
                data_to_send.set('kanban_column',self_modal['dataset']['kanbanColumn']);

                // Use axios to send data
                axios.post(
                    `${this.rootUrl}kanban_information/${this.locationId}/${this.objectModel.toLowerCase()}/add_link/`,
                    data_to_send,
                ).then(response => {
                    //Data has been successfully saved. Time to add the card to the board
                    this.$emit('new_card',response['data']);

                    //Clear the object model
                    this.objectModel = null;

                    //Click on the close button - a hack, but it should close the modal
                    document.getElementById("requirementLinkCloseButton").click();
                });
            }
        },
        watch: {
            objectModel: function() {
                //Clear data
                this.linkModel = [];

                //User has chosen an object.
                if (this.objectModel === null) {
                    //Ok - then removed the objects. We don't need to do anything
                    this.isSearching = false;
                    return;
                }

                //Tell the form that we are searching
                this.isSearching = true;

                //Now to use axios to get the data we require
                axios.post(
                    `${this.rootUrl}kanban_information/${this.locationId}/${this.objectModel}/link_list/`
                ).then(response => {
                    //Load the data into the array
                    this.objectResults = response['data'];

                    //Tell the user we are no longer searching
                    this.isSearching = false;
                }).catch(error => {
                    this.showErrorModal(error,'kanban');
                })
            },
            linkModel: function() {

            }
        }
    }
</script>

<style scoped>

</style>
