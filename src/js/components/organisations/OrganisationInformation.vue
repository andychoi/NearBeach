<template>
    <div class="card">
        <div class="card-body">
            <!-- TITLE -->
            <h1>Organisation Information</h1>
            <hr>

            <!-- FIELDS SECTION -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Please Note</strong>
                    <p class="text-instructions">
                        Please only use generic information for both the website and email. Do not use any personal
                        details - you can create contacts in the section below.
                    </p>
                </div>
                <div class="col-md-3">
                    <img v-bind:src="`${staticUrl}/NearBeach/images/placeholder/product_tour.svg`"
                         alt="No Profile Picture"
                         class="organisation-profile-image"
                    />
                    <br/>
                    <!--<button class="btn btn-primary">Update Profile...</button>-->
                    <n-upload
                        :action="`${rootUrl}organisation_information/${organisationResults[0]['pk']}/update_profile/`"
                        :headers="{
                            'X-CSRFTOKEN': getToken('csrftoken'),
                        }"
                        :data="{}"
                    >
                        <n-button>Update Profile Picture</n-button>
                    </n-upload>
                </div>
                <div class="col-md-5">
                    <!-- ORGANISATION NAME -->
                    <div class="form-group">
                        <label for="id_organisation_name">
                            Organisation Name
                            <span class="error"
                                  v-if="v$.organisationNameModel.$error.length > 0"
                                > Please suppy a title.
                            </span>
                        </label>
                        <input id="id_organisation_name"
                               v-model="organisationNameModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- ORGANISATION WEBSITE -->
                    <div class="form-group">
                        <label for="id_organisation_website">
                            Organisation Website
                            <span class="error"
                                  v-if="v$.organisationWebsiteModel.$error.length > 0"
                                  > Please supply a properly formatted URL
                            </span>
                        </label>
                        <input id="id_organisation_website"
                               v-model="organisationWebsiteModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- ORGANISATION EMAIL -->
                    <div class="form-group">
                        <label for="id_organisation_email">
                            Organisation Email
                            <span class="error"
                                  v-if="v$.organisationEmailModel.$error.length > 0"
                                  > Please supply a valid Email
                            </span>
                        </label>
                        <input id="id_organisation_email"
                               v-model="organisationEmailModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                </div>
            </div>
            <br/>

            <!-- NEED TO APPLY PERMISSIONS -->
            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateOrganisation"
                    >Update Organisation</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    //import { NButton, NUpload } from 'naive-ui';
    import { NButton, NUpload } from 'naive-ui';

    //VueX
    import { mapGetters } from 'vuex';

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { email, maxLength, required , url } from '@vuelidate/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";
    import getToken from "../../mixins/getTokenMixin";

    export default {
        name: "OrganisationInformation",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            NButton,
            NUpload,
        },
        props: {
            organisationResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        mixins: [
            errorModalMixin,
            getToken,
            loadingModalMixin,
        ],
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
        },
        data() {
            return {
                organisationNameModel: this.organisationResults[0]['fields']['organisation_name'],
                organisationEmailModel: this.organisationResults[0]['fields']['organisation_email'],
                organisationWebsiteModel: this.organisationResults[0]['fields']['organisation_website'],
            }
        },
        validations: {
            organisationNameModel: {
                required,
                maxLength: maxLength(255),
            },
            organisationWebsiteModel: {
                required,
                url,
            },
            organisationEmailModel: {
                required,
                email,
            },
        },
        methods: {
            updateOrganisation: function() {
                //Check validation
                this.v$.$touch();

                if (this.v$.$invalid) {
                    this.showValidationErrorModal();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Construct the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('organisation_name',this.organisationNameModel);
                data_to_send.set('organisation_email',this.organisationEmailModel);
                data_to_send.set('organisation_website',this.organisationWebsiteModel);

                //Show the loader
                this.showLoadingModal('Organisation');

                //Use axios to send the data
                axios.post(
                    `${this.rootUrl}organisation_information/${this.organisationResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error,'organisation',this.organisationResults[0]['pk']);
                })
            },
        }
    }
</script>

<style scoped>

</style>
