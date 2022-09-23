<template>
	<span>
		<!-- Recent Time -->
		<timeago v-if="isRecent(this.timestamp) || this.ago" :datetime="this.timestamp" :uk-tooltip="'title: ' + time.getReadableDate(this.timestamp)"/>

		<!-- Full Time -->
		<template v-else>
			<span v-if="this.short" :uk-tooltip="'title: ' + time.getReadableDate(this.timestamp)">
				{{ time.getShortReadableDate(this.timestamp) }}
			</span>
			<span v-else>
				{{ time.getReadableDate(this.timestamp) }}
			</span>
		</template>
	</span>
</template>

<script>
	export default {
		data() {
			return {
				time: require('~/assets/script/time.js')
			}
		},
		props: {
			timestamp: {
				type: Number,
				required: true
			},
			short: {
				type: Boolean,
				required: false,
				default: false
			},
			ago: {
			    type: Boolean,
				required: false,
				default: false
			}
		},
		methods: {
			isRecent(time) {
				return Date.now() - time <= 604800000
			},
		}
	}
</script>
