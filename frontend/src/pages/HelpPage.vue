<template>
  <div class="conta">
    <header class="header2">
      <svg class="gene-title" viewBox="0 0 1000 100">
        <text x="50%" y="50%" text-anchor="middle" dy=".35em" class="gene-text">About Us</text>
      </svg>
    </header>

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
        <button class="btn btn-primary" @click="openModal"> <i class="fas fa-phone"></i>   Contact Us</button>
      </div>

      <!-- Modal -->
      <div class="modal fade" id="contactModal" tabindex="-1" aria-labelledby="contactModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="contactModalLabel"><i class="fas fa-phone"></i>   Contact Us</h5>
              <button type="button" class="custom-close" data-bs-dismiss="modal" aria-label="Close">&times;</button>
            </div>
            <div class="modal-body">
              <div class="d-flex flex-wrap justify-content-center text-center">
                <div class="row">
                  <div class="col-6 p-3 member-card" v-for="(member, index) in teamMembers" :key="index">
                    <div class="luxurious-frame">
                      <img :src="member.image" class="luxurious-img" alt="Team member">
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
                      <!-- <span class="icon">
                        <i class="fas fa-phone"></i>
                      </span> -->
                    </div>
                  </div>
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
          image: require('@/assets/ayelet.png'),
          name: 'AYELET MOYAL',
          role: 'Project Lead + Frontend Developer',
          linkedin: 'https://www.linkedin.com/in/john-doe',
          email: 'ayelet431@mail.com',
        },
        {
          image: require('@/assets/natalia.jpeg'),
          name: 'NATALIA KATAEV',
          role: 'Backend Developer',
          linkedin: 'https://www.linkedin.com/in/jane-smith',
          email: 'jane.smith@mail.com',
        },
        {
          image: require('@/assets/fish.png'),
          name: 'Assaf Shokroon',
          role: 'Frontend Developer',
          linkedin: 'https://www.linkedin.com/in/alice-johnson',
          email: 'alice.johnson@mail.com',
        },
        {
          image: require('@/assets/fish.png'),
          name: 'Maor Biton',
          role: 'Data Scientist',
          linkedin: 'https://www.linkedin.com/in/bob-brown',
          email: 'bob.brown@mail.com',
        },
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
.conta {
  position: relative;
  overflow: hidden;
}

.conta::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('../assets/evo5.jpg') no-repeat center center fixed;
  background-size: cover;
  opacity: 0.3;
}


.header2{
  opacity: 0.99;
}

.container {
  width: 90%;
  max-width: 900px;
  margin: 5vh auto;
  padding: 3vw;
  border: 0.3vw solid #ebebeb;
  background-color: rgba(244, 244, 244, 0.8); /* Adjusted opacity for transparency */
  border-radius: 2vw;
  box-shadow: 0.5vw 0.5vw 1vw rgba(144, 143, 143, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box; /* Ensures padding and border are included in the element's total width and height */
  position: relative;
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

.luxurious-frame {
  position: relative;
  width: 140px; /* Adjust width for larger image */
  height: 140px; /* Adjust height for larger image */
  padding: 3px;
  background: linear-gradient(145deg, #444, #000); /* Luxurious gradient background */
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5), inset 0 0 10px rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  overflow: hidden; /* Ensures images stay within the frame */
}

.luxurious-frame:before,
.luxurious-frame:after {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  border: 5px solid #fff;
  border-radius: 50%;
  top: -10px;
  left: -10px;
  z-index: -1;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.luxurious-frame:after {
  top: 10px;
  left: 10px;
  z-index: -2;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
}

.luxurious-img {
  width: 100%; /* Ensure the image fits within the frame */
  height: 100%;
  object-fit: cover; /* Ensures the image covers the frame without distortion */
  border-radius: 50%;
  transition: transform 0.3s ease-in-out;
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
  color: #d46b09;
}

.icon:hover {
  color: #ff9028;
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

.luxurious-frame:hover .luxurious-img {
  transform: scale(1.2);
}

.btn-primary {
  font-size: 1.5rem; /* Make the button text larger */
  padding: 0.75rem 2rem; /* Adjust padding for a larger button */
  background-color: #166844; /* Primary color */
  border: 0.1em solid hsl(186, 54%, 19%);
  border-radius: 50px; /* Elliptical shape */
  transition: all 0.3s ease-in-out;
}

.btn-primary:hover {
  background-color: #22a66d; /* Darker shade on hover */
  transform: scale(1.1); /* Slightly larger on hover */
  border: 0.1em solid hsl(186, 54%, 19%);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Add a shadow effect on hover */
}
</style>
