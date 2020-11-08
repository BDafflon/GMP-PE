<template>
	<div>
		<section ref="chatArea" class="chat-area" id="chatroom">
			<p
				v-for="message in messages"
				:key="message.id_action"
				class="message"
				:class="{
					'message-out': message.id_etudiant === user.id,
					'message-in': message.id_etudiant !== user.id
				}"
			>
				{{ message.action }}
			</p>
		</section>
		<section class="">
			<form @submit.prevent="sendMessage('out')" id="person2-form">
				<div class="row">
					<div class="col-sm-8">
						<input
							v-model="youMessage"
							type="text"
							id="person2-input"
							class="form-control"
							placeholder="Message"
							required
							autofocus
						/>
					</div>
					<div class="col-sm-4">
						<button class="btn  btn-primary btn-block" type="submit">Envoyer</button>
					</div>
				</div>
			</form>
		</section>
	</div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";

export default {
	name: "Chat",
	props: ["candidature"],
	watch: {
		// This would be called anytime the value of title changes
		candidature(newValue, oldValue) {
			console.debug(oldValue);
			this.candidature = newValue;
			this.clearAllMessages();
			this.fetchData();
		}
	},
	data() {
		return {
			bobMessage: "",
			youMessage: "",
			messages: [
				{
					id: 1,
					body: "Welcome to the chat, I'm Bob!",
					author: "bob"
				},
				{
					id: 2,
					body: "Thank you Bob",
					author: 1
				},
				{
					id: 3,
					body: "You're most welcome",
					author: "bob"
				}
			]
		};
	},
	computed: {
		...mapState([
			"apiurl",
			"loggingIn",
			"loginError",
			"accessToken",
			"logged",
			"user"
		])
	},
	created() {
		this.fetchData();
	},
	methods: {
		scrollToEnd: function() {
			var container = document.querySelector("#chatroom");
			container.scrollTop = container.scrollHeight;
		},
		sendMessage(direction) {
			console.debug(this.messages);
			if (!this.youMessage && !this.bobMessage) {
				return;
			}
			if (direction === "out") {
				this.addData(this.youMessage);
				this.youMessage = "";
			} else {
				alert("something went wrong");
			}

			this.$nextTick(() => this.scrollToEnd());
		},
		clearAllMessages() {
			this.messages = [];
		},
		addData(message) {
			console.debug(message);
			axios({
				method: "post",
				url: "actionpe/registration",
				data: {
					action: message,
					id_etudiant: this.user.id,
					id_candidature: this.candidature.id_candidature
				},
				auth: {
					username: this.user.mail,
					password: this.user.pwd
				}
			})
				.then(response => {
					this.messages.push({
						id_action: response.id_action,
						action: message,
						id_etudiant: this.user.id,
						id_candidature: this.candidature.id_candidature
					});
				})
				.catch(error => {
					console.debug(error);
				});
		},
		fetchData() {
			axios({
				method: "get",
				url: "actionpe/" + this.candidature.id_candidature,
				auth: {
					username: this.user.mail,
					password: this.user.pwd
				}
			})
				.then(response => {
					this.messages = response.data;
					this.candidature.ap = 0;
				})
				.catch(error => {
					console.debug(error);
				});
		}
	}
};
</script>

<style lang="scss">
@import "../assets/custom.scss";
@import "node_modules/bootstrap/scss/bootstrap.scss";
@import "../assets/sb-admin-2.min.css";

.chat-area {
	/*   border: 1px solid #ccc; */
	background: white;
	max-height: 30vh;
	padding: 1em;
	overflow: auto;

	margin: 0 auto 2em auto;
}
.message {
	width: 50%;
	border-radius: 10px;
	padding: 0.5em;
	/*   margin-bottom: .5em; */
	font-size: 0.8em;
}
.message-out {
	background: #407fff;
	color: white;
	margin-left: 50%;
	text-align: right;
}
.message-in {
	background: #f1f0f0;
	color: black;
	text-align: left;
}
.chat-inputs {
	display: flex;
	justify-content: space-between;
}
</style>
