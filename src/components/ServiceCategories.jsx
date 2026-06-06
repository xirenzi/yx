import { serviceCategories } from "../content.js";
import SectionTitle from "./SectionTitle.jsx";
import ServiceCard from "./ServiceCard.jsx";

export default function ServiceCategories({ onContact }) {
  return (
    <section className="page-section" id="services">
      <SectionTitle
        eyebrow="Services"
        title="服务分类"
        description="根据不同需求选择对应服务，具体规则以下单详情和客服确认为准。"
      />

      <div className="service-grid">
        {serviceCategories.map((service) => (
          <ServiceCard key={service.name} service={service} onContact={onContact} />
        ))}
      </div>
    </section>
  );
}
