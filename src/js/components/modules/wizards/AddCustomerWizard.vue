<template>
    <div class="modal fade" id="addCustomerModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><Icon v-bind:icon="icons.usersIcon"></Icon> Add Customers Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="addCustomerCloseButton"
                    >
                        <span aria-hidden="true"></span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row" v-if="customerFixList.length > 0">
                        <div class="col-md-4">
                            <strong>Select Customer</strong>
                            <p class="text-instructions">
                                Search for a customer who has not been added to this {{destination}}. If the search is
                                blank there are either no customers that match that search, or all customer have already
                                been added to the {{destination}}.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <n-select :options="customerFixList"
                                label="customerName"
                                v-model:value="customerModel"
                            ></n-select>
                        </div>
                    </div>
                    <div class="row" v-else>
                        <div class="col-md-6">
                            <strong>Sorry - no results</strong>
                            <p class="text-instructions">
                                This could be because
                                <ul>
                                    <li>There are no more customers left to add</li>
                                    <li>There are no customers for this organisation</li>
                                </ul>
                            </p>
                        </div>
                        <div class="col-md-6 no-search">
                            <img v-bind:src="`${staticUrl}NearBeach/images/placeholder/questions.svg`"
                                 alt="Sorry - there are no results"
                            />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:diabled="customerModel == ''"
                            v-on:click="addCustomer"
                    >
                        Save changes
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { Icon } from '@iconify/vue';
    import { NSelect } from 'naive-ui';

    //Mixins
    import errorModalMixin from "../../../mixins/errorModalMixin";
    import iconMixin from "../../../mixins/iconMixin";

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "AddCustomerWizard",
        components: {
            Icon,
            NSelect,
        },
        props: {
            destination: {
                type: String,
                default: '',
            },
            locationId: {
                type: Number,
                default: 0,
            },
            excludeCustomers: {
                type: Array,
                default: () => {
                    return [];
                },
            }
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            })
        },
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                customerModel: '',
                customerList: [],
                customerFixList: [],
            }
        },
        methods: {
            addCustomer: function() {
                // Set up the data object to send
                const data_to_send = new FormData();
                data_to_send.set('customer', this.customerModel);

                axios.post(
                    `${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_customer/`,
                    data_to_send,
                ).then((response) => {
                    //Send the new data up stream
                    this.$emit('update_customer_results',response['data']);

                    //Clear the model
                    this.customerModel = '';

                    //Close the modal
                    document.getElementById("addCustomerCloseButton").click();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            getCustomerList: function() {
                axios.post(
                    `${this.rootUrl}object_data/${this.destination}/${this.locationId}/customer_list_all/`,
                ).then(response => {
                    //Place all the data into the "CustomerList" array.
                    this.customerList = response['data'];

                    //Update the fixed list
                    this.updateCustomerFixList();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            updateCustomerFixList: function() {
                //If no customer list result - just exit
                if (this.customerList.length === 0) return;

                //Create an array of ids we should be excluding
                var exclude_array = [];
                this.excludeCustomers.forEach(row => {
                    exclude_array.push(row['pk']);
                });

                //Set the customerFixList
                this.customerFixList = this.customerList.filter(row => {
                    return !exclude_array.includes(row['pk']);
                }).map(row => {
                    return {
                        value: row['pk'],
                        label: `${row['fields']['customer_first_name']} ${row['fields']['customer_last_name']}`,
                    }
                });
            },
        },
        mounted() {
            //If the location is inside the array - don't bother getting the data
            var escape_array = [
                'requirement_item',
            ]
            if (escape_array.indexOf(this.locationId) < 0) return;

            //Wait 200ms before getting data
            setTimeout(() => {
                this.getCustomerList();
            }, 200);
        },
        watch: {
            excludeCustomers: function(){
                this.updateCustomerFixList();
            },
        }
    }
</script>

<style scoped>

</style>
