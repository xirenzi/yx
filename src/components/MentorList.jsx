import { mentors } from "../content.js";
import SectionTitle from "./SectionTitle.jsx";
import MentorCard from "./MentorCard.jsx";

export default function MentorList() {
  return (
    <section className="page-section" id="mentors">
      <SectionTitle
        eyebrow="Mentors"
        title="电竞导师名单"
        description="专业导师协作，按规则执行护航服务。"
      />

      <div className="mentor-grid">
        {mentors.map((mentor, index) => (
          <MentorCard mentor={mentor} index={index} key={mentor.name} />
        ))}
      </div>
    </section>
  );
}
