export default function ServiceCard({ service, onContact }) {
  return (
    <article className="service-card reveal">
      <div className="card-head">
        <h3>{service.name}</h3>
        <span>{service.tag}</span>
      </div>
      <p>{service.description}</p>
      <button className="text-button" type="button" onClick={onContact}>
        咨询详情
      </button>
    </article>
  );
}
