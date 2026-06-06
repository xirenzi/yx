export default function MentorCard({ mentor, index }) {
  return (
    <article className="mentor-card reveal">
      <div className={`mentor-avatar avatar-${(index % 4) + 1}`}>{mentor.name[0]}</div>
      <div>
        <div className="mentor-heading">
          <h3>{mentor.name}</h3>
          <span>{mentor.tag}</span>
        </div>
        <p>{mentor.bio}</p>
      </div>
    </article>
  );
}
