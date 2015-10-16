ALTER TABLE "main_app_userprofile" ADD COLUMN "secret_key" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_code" TYPE varchar(30);

ALTER TABLE "main_app_userprofile" DROP COLUMN "user_code" CASCADE;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_email" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_email" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "profile_password" varchar(30) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "profile_password" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "token" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "token" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "uid" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "uid" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ADD COLUMN "user_key" varchar(50) DEFAULT '' NOT NULL;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "user_key" DROP DEFAULT;
ALTER TABLE "main_app_userprofile" ALTER COLUMN "secret_key" TYPE varchar(50);

ALTER TABLE "main_app_userprofile" DROP CONSTRAINT "main_app_userp_schema_id_4cddfcbff18e38b1_fk_main_app_schema_id";
ALTER TABLE "main_app_userprofile" DROP COLUMN "schema_id" CASCADE;
DROP TABLE "main_app_schema" CASCADE;

-- Create call teble - 15.10.2015 --
CREATE TABLE "main_app_call" (
	"id" serial NOT NULL PRIMARY KEY,
	"call_id" varchar(30) NOT NULL,
	"sip" varchar(20) NOT NULL,
	"date" timestamp with time zone NOT NULL,
	"destination" varchar(30) NOT NULL,
	"description" varchar(100) NOT NULL,
	"disposition" varchar(20) NOT NULL,
	"bill_seconds" integer NOT NULL,
	"cost" double precision NOT NULL,
	"bill_cost" double precision NOT NULL,
	"currency" varchar(20) NOT NULL,
	"user_profile_id" integer NOT NULL);
ALTER TABLE "main_app_call" ADD CONSTRAINT "main_app_ca_user_profile_id_586a6b3e_fk_main_app_userprofile_id" FOREIGN KEY ("user_profile_id") REFERENCES "main_app_userprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "main_app_call_06037614" ON "main_app_call" ("user_profile_id");
-- --