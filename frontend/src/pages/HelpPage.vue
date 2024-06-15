<template>
  <div class="container">
    <h1 class="title">Comprehensive End-to-End Gene Visualization System - "Evo-Genes"</h1>
    <p>
      As part of our final project in the Department of Software and Information Systems Engineering at Ben Gurion University of the Negev, under the guidance of Prof. Guy Shani from the Faculty of Software and Information Systems Engineering and Dr. Tal Shay from the Faculty of Life Sciences, we have developed a comprehensive end-to-end gene visualization system. The laboratory aims to unravel the complexity of how cells with identical genetic information can exhibit diverse functions and phenotypic properties. 
    </p>
    <p>
      A significant challenge in this research is the limited capability to compare gene similarities across species while maintaining the context of the original gene structure.
    </p>
    <p>
      Currently, no system allows for the simultaneous examination of sequence similarities and structural differences between species. To address this challenge, we have created a web-based system that leverages both server-side and client-side programming to interface with the extensive Ensembl database.
    </p>
    <p>
      Our system facilitates intuitive and visually engaging comparative gene sequence analysis, emphasizing the display of exons, thus optimizing comparative gene analysis. This unique feature significantly enhances the accessibility and utility of gene comparison tools, providing biologists and researchers with comprehensive insights into gene development and functional divergence. The system streamlines the comparative analysis process by automating sequence retrieval and aligning gene structures with Dot Plot outputs, thereby boosting research productivity and data analysis efficiency.
    </p>
    <p>
      We have invested considerable effort in the design and development of the system, ensuring a professional and attractive user experience, which is integral to its overall functionality.
    </p>
    <div class="text-center mt-5">
      <button class="btn btn-primary" @click="openModal">Contact Us</button>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="contactModal" tabindex="-1" aria-labelledby="contactModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="contactModalLabel">Contact Us</h5>
            <button type="button" class="custom-close" data-bs-dismiss="modal" aria-label="Close">&times;</button>
          </div>
          <div class="modal-body">
            <div class="d-flex flex-wrap justify-content-center text-center">
              <div class="p-3 member-card" v-for="(member, index) in teamMembers" :key="index">
                <div class="image-frame">
                  <img :src="member.image" class="rounded-circle img-thumbnail mb-3" alt="Team member">
                </div>
                <h5>{{ member.name }}</h5>
                <p class="role">{{ member.role }}</p>
                <div class="contact-icons">
                  <a :href="member.linkedin" target="_blank" class="icon">
                    <i class="fab fa-linkedin"></i>
                  </a>
                  <a :href="'mailto:' + member.email" class="icon">
                    <i class="fas fa-envelope"></i>
                  </a>
                  <span class="icon">
                    <i class="fas fa-phone"></i> {{ member.phoneNumber }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';

export default {
  name: 'AboutComp',
  data() {
    return {
      teamMembers: [
        {
          image: require('@/assets/fish.png'),
          name: 'John Doe',
          role: 'Project Lead',
          linkedin: 'https://www.linkedin.com/in/john-doe',
          email: 'john.doe@mail.com',
          phoneNumber: '+1 (234) 567-890'
        },
        {
          image: require('@/assets/fish.png'),
          name: 'Jane Smith',
          role: 'Backend Developer',
          linkedin: 'https://www.linkedin.com/in/jane-smith',
          email: 'jane.smith@mail.com',
          phoneNumber: '+1 (234) 567-891'
        },
        {
          image: require('@/assets/fish.png'),
          name: 'Alice Johnson',
          role: 'Frontend Developer',
          linkedin: 'https://www.linkedin.com/in/alice-johnson',
          email: 'alice.johnson@mail.com',
          phoneNumber: '+1 (234) 567-892'
        },
        {
          image: require('@/assets/fish.png'),
          name: 'Bob Brown',
          role: 'Data Scientist',
          linkedin: 'https://www.linkedin.com/in/bob-brown',
          email: 'bob.brown@mail.com',
          phoneNumber: '+1 (234) 567-893'
        }
      ]
    };
  },
  methods: {
    openModal() {
      var myModal = new Modal(document.getElementById('contactModal'));
      myModal.show();
    }
  }
};
</script>

<style scoped>
.container {
  width: 90%;
  max-width: 900px;
  margin: 5vh auto;
  padding: 3vw;
  border: 0.3vw solid #ebebeb;
  background-color: rgba(244, 244, 244, 0.6);
  border-radius: 2vw;
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box; /* Ensures padding and border are included in the element's total width and height */
}

.title {
  text-align: center;
  margin-bottom: 40px; /* Increase space below the title */
  font-size: 23px;
}

p {
  margin-bottom: 20px; /* Adds space between paragraphs */
  text-align: justify; /* Justifies text for a cleaner look */
  font-size: 18px; /* Sets the font size for the paragraphs */
  line-height: 1.6; /* Adjusts line spacing for better readability */
}

.image-frame {
  border: 5px solid #ddd; /* Add a border to the image frame */
  border-radius: 50%; /* Make the frame circular */
  padding: 5px; /* Add padding inside the frame */
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3); /* Add shadow for a luxurious effect */
  width: 100px; /* Adjust width for smaller image */
  height: 100px; /* Adjust height for smaller image */
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin: 0 auto; /* Center the frame */
}

.image-frame img {
  width: 90%; /* Ensure the image fits within the frame */
  height: auto; /* Maintain aspect ratio */
}

.member-card {
  text-align: center;
}

.role {
  text-align: center; /* Center the role text */
  margin-top: -10px; /* Adjust margin to position the role closer to the name */
}

.contact-icons {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.icon {
  margin: 0 10px;
  font-size: 20px;
  color: #007bff;
}

.icon:hover {
  color: #0056b3;
}

.modal-content {
  background-color: #f8f9fa;
  border-radius: 1rem;
}

.modal-header {
  border-bottom: none;
  position: relative;
}

.custom-close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  color: #000;
  cursor: pointer;
  border: none;
  background: none;
}

.custom-close:hover {
  color: #ff0000;
}

.modal-dialog {
  max-width: 800px;
}

.modal-body {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5); /* Ensures the backdrop darkens the background */
}

.modal-title {
  text-align: center;
  width: 100%;
}
</style>
