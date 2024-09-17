<template>
  <div class="conta">
    <header class="header2">
      <svg class="gene-title" viewBox="0 0 1000 100">
        <text x="50%" y="50%" text-anchor="middle" dy=".35em" class="gene-text">About Us</text>
      </svg>
    </header>

    <div class="container">
      <h1 class="title">Gene structure and sequence comparison visualization system - "Evo-Genes"</h1>
      <p>
        The “Evo-Genes” application aims to visualize gene sequence conservation associated with gene structure. For this purpose, the dot-plot of the sequences is presented alongside the gene structure diagrams depicting exons (rectangles) and introns (lines).      </p>
      <p>
        The input is the Ensembl ID of the two genes to be compared. By default, the consensus transcript, as defined by Ensembl, is presented for each of the genes. The user can choose different transcripts of each of the two genes from a drop-down menu.  The user can also zoom-in to regions of interest, by either marking the regions or typing the coordinates within the genes.       </p>
      <p>
        As the dot-plot of long genes can be much larger than can be presented on the screen, the subsampling option allows for a smaller version, to make run time shorter. This option is recommended for large genes.        </p>
      <p>
        This unique visualization enables identifying changes in gene structure, for example exon split into several exons, addition of novel sequences, exon duplication etc.    </p>
        <p>
    The dotplot is produced by the Yass algorithm <sup>[1]</sup>, implementation version 1.16, downloaded from 
    <a href="https://github.com/laurentnoe/yass" target="_blank">https://github.com/laurentnoe/yass</a>.
</p>

      <p><strong>Developers:</strong>
        </p>
        <p>
•	This application was developed as part of a final project in the Department of Software and Information Systems Engineering at Ben-Gurion University of the Negev, under the guidance of Prof. Guy Shani from the department of Software and Information Systems Engineering and Dr. Tal Shay from the department of Life Sciences.

      </p>
      <p><strong>References:</strong></p>
      <p>
        1.	L. Noe, G. Kucherov YASS: enhancing the sensitivity of DNA similarity search, 2005, Nucleic Acids Research, 33(2):W540-W543.
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
          linkedin: 'https://www.linkedin.com/in/ayelet-moyal-36748720b/',
          email: 'ayelet431@mail.com',
        },
        {
          image: require('@/assets/natalia.jpeg'),
          name: 'NATASHA KATAEV',
          role: 'Backend Developer',
          linkedin: 'https://www.linkedin.com/in/natasha-kataev-b47406158/',
          email: 'nat.kataev@gmail.com',
        },
        {
          image: require('@/assets/assaf.jpg'),
          name: 'Assaf Shukrun',
          role: 'Fullstack Developer',
          linkedin: 'https://www.linkedin.com/in/assaf-shukrun/',
          email: 'assaf7070@gmail.com',
        },
        {
          image: require('@/assets/maor.png'),
          name: 'Maor Biton',
          role: 'Backend Developer',
          linkedin: 'https://www.linkedin.com/in/maor-biton-449136232/',
          email: 'maor20561@gmail.com',
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
