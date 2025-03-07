<template>
    <div class="row">
        <div class="col-md-4">
            <strong>Between Dates</strong>
            <p class="text-instructions">
                Choose the start and end date of the {{destination}}. Please note the end date can not be earlier than
                the start date. They can be equal.
            </p>
        </div>
        <div class="col-md-4">
            <div class="form-group">
                <label>{{destination}} Start Date:
                    <span class="error"
                          v-if="!v$.localStartDateModel.$error.length > 0"
                    > Please select a date.</span>
                </label>
                <n-date-picker type="datetime"
                               v-model:value="localStartDateModel"
                               class="form-control"
                ></n-date-picker>
            </div>
        </div>
        <div class="col-md-4">
            <div class="form-group">
                <label>{{destination}} End Date:
                    <span class="error"
                          v-if="!v$.localEndDateModel.$error.length > 0"
                    > Please select a date.</span>
                </label>
                <n-date-picker type="datetime"
                               v-model:value="localEndDateModel"
                               class="form-control"
                ></n-date-picker>
            </div>
        </div>
    </div>
</template>

<script>
    import { NDatePicker } from 'naive-ui';

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required } from '@vuelidate/validators'

    export default {
        name: "BetweenDates",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            NDatePicker,
        },
        props: {
            destination: {
                type: String,
                default: "",
            },
            endDateModel: {
                type: Number,
                default: () => {
                    let temp_date = new Date();
                    temp_date.setHours(16);
                    temp_date.setMinutes(0);
                    temp_date.setSeconds(0);
                    temp_date.setMilliseconds(0);

                    //Add on 14 days
                    new Date(temp_date.setDate(temp_date.getDate() + 14));

                    return temp_date.getTime();
                },
            },
            startDateModel: {
                type: Number,
                default: () => {
                    let temp_date = new Date();
                    temp_date.setHours(9);
                    temp_date.setMinutes(0);
                    temp_date.setSeconds(0);
                    temp_date.setMilliseconds(0);

                    return temp_date.getTime();
                },
            },
        },
        validations: {
            localEndDateModel: {
                required,
            },
            localStartDateModel: {
                required,
            },
        },
        data() {
            return {
                localEndDateModel: this.endDateModel,
                localStartDateModel: this.startDateModel,
            }
        },
        methods: {
            emitDates: function() {
                //Send this data upstream
                this.$emit('update_dates',{
                    'start_date': this.localStartDateModel,
                    'end_date': this.localEndDateModel
                })
            },
        },
        watch: {
            localEndDateModel: function() {
                //Makes sure the end date is not less than the start date
                // - if it is, turn it into the start date
                if (this.localEndDateModel < this.localStartDateModel) {
                    //The Start date is larger than the end date - make it the same
                    this.localEndDateModel = this.localStartDateModel();
                }

                //Send the new results up steam
                this.emitDates();
            },
            localStartDateModel: function() {
                //Makes sure the start date is not greater than the end date
                // - if it is, turn it into the end date
                if (this.localEndDateModel < this.localStartDateModel) {
                    //The Start date is larger than the end date - make it the same
                    this.localStartDateModel = this.localEndDateModel();
                }

                //Send the new results up stream
                this.emitDates();
            },
        },
        mounted() {
            //In case the dates fall on default - send up stream
            this.emitDates();
        },
    }
</script>

<style scoped>

</style>