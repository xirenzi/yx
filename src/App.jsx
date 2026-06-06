import Header from "./components/Header.jsx";
import HeroSection from "./components/HeroSection.jsx";
import ServiceCategories from "./components/ServiceCategories.jsx";
import OrderNotice from "./components/OrderNotice.jsx";
import MentorList from "./components/MentorList.jsx";
import RecruitSection from "./components/RecruitSection.jsx";
import ContactSection from "./components/ContactSection.jsx";
import Footer from "./components/Footer.jsx";
import MobileFloatingCTA from "./components/MobileFloatingCTA.jsx";
import { scrollToSection } from "./utils/scroll.js";

export default function App() {
  const goToContact = () => scrollToSection("contact");

  return (
    <>
      <Header onContact={goToContact} />
      <main>
        <HeroSection onContact={goToContact} />
        <ServiceCategories onContact={goToContact} />
        <OrderNotice />
        <MentorList />
        <RecruitSection onContact={goToContact} />
        <ContactSection />
      </main>
      <Footer />
      <MobileFloatingCTA onContact={goToContact} />
    </>
  );
}
